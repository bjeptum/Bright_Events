"""
Blueprint module
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """ Initialize Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    """ Initialize extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    """ Import and register blueprints"""
    from .routes.auth import auth_bp
    from .routes.events import events_bp
    from .routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(main_bp)
    
    return app
