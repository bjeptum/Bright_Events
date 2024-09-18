"""
Main Routes Module
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Show the home page"""    
    return render_template('index.html')
