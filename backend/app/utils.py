from .models import User
from . import login_manager 
"""
Utility functions for password hashing
and verification using Werkzeug
"""
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

@login_manager.user_loader
def load_user(user_id):
    """Reload user object from user id stored in the session"""
    return User.query.get(int(user_id))
