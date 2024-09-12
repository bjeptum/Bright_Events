"""
Contains the main routes
Show the homepage and event-related pages
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from flask_login import login_required, current_user
from ..models import db, Event, EventCategory
from ..forms import EventForm

main_bp = Blueprint('main', __name__)
events_bp = Blueprint('events', __name__)

@main_bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_bp.route('/events')
def list_events():
    events = Event.query.all()
    return render_template('event_list.html', events=events)

@main_bp.route('/events/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@main_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            category_id=form.category.data,
            organizer_id=current_user.id  # Assuming current_user has an id attribute
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('main.view_event', event_id=event.id))
    return render_template('event_form.html', form=form)

@main_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        flash('You are not authorized to edit this event.')
        return redirect(url_for('main.view_event', event_id=event_id))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.location = form.location.data
        event.category_id = form.category.data
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('main.view_event', event_id=event.id))
    return render_template('event_form.html', form=form, event=event)
