"""
Blueprint module
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    """ Initialize Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])


    """ Initialize extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Specify login view for @login_required
    
    """ Import and register blueprints"""
    from .routes.auth import auth_bp
    from .routes.events import events_bp
    from .routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(main_bp)
    return app

# Define the user loader callback
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))