"""
Blueprint module
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """ Initialize Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.events import events_bp
    from .routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(main_bp)

    # Load user
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
