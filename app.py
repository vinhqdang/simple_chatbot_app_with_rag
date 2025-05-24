from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db
import config
from auth import auth_bp
from chat import chat_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    
    for rule in app.url_map.iter_rules():
        print(rule.endpoint, rule)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
