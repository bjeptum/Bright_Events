"""
Contains the main route
Show the homepage
"""
from . import main_bp
from flask import render_template
from ..models import Event

@main_bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)
