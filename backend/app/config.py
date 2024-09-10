import os

class Config(object):
    """ Parent configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """ Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite3:///dev_db.sqlite')

class TestingConfig(Config):
    """ Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite3:///test_db.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI', 'sqlite:///prod_db.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
