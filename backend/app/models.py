"""
Database Schema
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model,UserMixin):
    """ Defines users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    organizer = db.relationship('Organizer', backref='user', uselist=False)
    attendee = db.relationship('Attendee', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organizer(db.Model):
    __tablename__ = 'organizers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    events = db.relationship('Event', backref='organizer', lazy=True)


class Attendee(db.Model):
    __tablename__ = 'attendees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rsvps = db.relationship('RSVP', backref='attendee', lazy=True)


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers.id'), nullable=False)
    rsvps = db.relationship('RSVP', backref='event', lazy=True)
    category = db.relationship('EventCategory', backref='events')


class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    events = db.relationship('Event', backref='category', lazy=True)


class RSVP(db.Model):
    __tablename__ = 'rsvps'
    
    id = db.Column(db.Integer, primary_key=True)
    attendee_id = db.Column(db.Integer, db.ForeignKey('attendees.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
