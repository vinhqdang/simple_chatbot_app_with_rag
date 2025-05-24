# Chatbot Application

## Setup

1. Create a conda environment:
   ```bash
   conda create -n chatbot python=3.10 -y
   conda activate chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API key:
   - Copy `config.json.example` to `config.json`
   - Edit `config.json` and set your OpenAI API key.
   - If you don't have an OpenAI key, leave it blank and select the HuggingFace provider when chatting.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access in browser at http://127.0.0.1:5000

## Features

- User registration and login
- Chatbot with GPT-4o multi-modal support (text and image)
- Session management: create and delete chat sessions
