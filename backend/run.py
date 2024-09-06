"""
Entry point for the Flask app
"""
from app import create_app, db
from flask_migrate import Migrate

app = create_app()

migrate = Migrate(app, db, command='migrate')

if __name__ == "__main__":
    app.run()
