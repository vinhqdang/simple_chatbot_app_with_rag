from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import openai, base64, uuid
import config
from models import db, ChatSession, Message

# NEW: import and init a HF pipeline
from transformers import pipeline

# Default system prompt, configurable via config.json
SYSTEM_PROMPT = getattr(config, 'SYSTEM_PROMPT', "You are a helpful assistant.")

# pick any HF conversational/text-generation model that's free to use
HF_MODEL = getattr(config, 'HF_MODEL', "meta-llama/Llama-2-7b-chat-hf")
hf_generator = pipeline('text-generation', model=HF_MODEL, trust_remote_code=True)

chat_bp = Blueprint('chat', __name__)

openai.api_key = config.API_KEY

@chat_bp.route('/chat', methods=['GET','POST'])
@login_required
def chat():
    if request.method == 'POST':
        session_id   = request.form.get('session_id')
        user_input   = request.form.get('message')
        provider     = request.form.get('provider', 'openai')  # NEW: provider toggle
        file         = request.files.get('image')

        session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
        if not session:
            flash('Session not found')
            return redirect(url_for('chat.chat'))

        # Save user text
        msg = Message(session_id=session.id, role='user', content=user_input)
        db.session.add(msg)
        db.session.commit()

        # Build context for OpenAI, if needed
        messages = []
        if provider == 'openai':
            # Start the conversation with the system prompt
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
            for m in session.messages:
                if m.content:
                    messages.append({"role": m.role, "content": m.content})
            # Add latest user message
            messages.append({"role": "user", "content": user_input})
            # Handle image (same as before)
            if file and file.filename:
                image_data = base64.b64encode(file.read()).decode('utf-8')
                messages.append({"role":"user","content": f"<image>{image_data}</image>"})
            # Call OpenAI
            resp = openai.chat.completions.create(model=config.MODEL, messages=messages)
            bot_reply = resp.choices[0].message.content

        else:  # provider == 'hf'
            # A simple HF flow: just feed the latest user message
            # (you could concatenate conversation history here too)
            prompt = f"{SYSTEM_PROMPT}\n{user_input}"
            generated = hf_generator(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
            # Remove the prompt from the generated text if echoed
            bot_reply = generated[len(prompt):].strip()

        # Save assistant reply
        bot_msg = Message(session_id=session.id, role='assistant', content=bot_reply)
        db.session.add(bot_msg)
        db.session.commit()

        # redirect back to the same session, preserving provider if you like
        return redirect(url_for('chat.chat', session_id=session.id, provider=provider))

    # GET handler: load sessions + conversation
    sessions = ChatSession.query.filter_by(user_id=current_user.id).all()
    session_id      = request.args.get('session_id')
    current_session = None
    messages        = []
    if session_id:
        current_session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
        if current_session:
            messages = current_session.messages

    # pass through the currently selected provider so the UI can default it
    provider = request.args.get('provider', 'openai')
    return render_template('chat.html',
                           sessions=sessions,
                           current_session=current_session,
                           messages=messages,
                           provider=provider)

@chat_bp.route('/session/new')
@login_required
def new_session():
    session = ChatSession(user_id=current_user.id, name=f"Session {uuid.uuid4().hex[:8]}")
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('chat.chat', session_id=session.id))

@chat_bp.route('/session/delete/<int:session_id>')
@login_required
def delete_session(session_id):
    session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if session:
        db.session.delete(session)
        db.session.commit()
    return redirect(url_for('chat.chat'))