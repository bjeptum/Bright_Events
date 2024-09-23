""""
Event Routes Module
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Event, RSVP, Organizer, Attendee
from flask_login import current_user, login_required
from flask_login import LoginManager
from ..forms import EventForm

events_bp = Blueprint('events', __name__)

# HTML Routes

@events_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event_form():
    """Creates a new event."""
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            description=form.description.data,
            # category_id=form.category.data, # Uncomment when category field is available
            organizer_id=current_user.id # Associate the event with current user
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('events.list_events_form'))
    return render_template('event_form.html', form=form)

@events_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event_form(event_id):
    """Edit an existing event"""
    event = Event.query.get_or_404(event_id)
    # Check if the current user is the organzer of the event
    if event.organizer_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('events.list_events_form'))

    form = EventForm(obj=event)
    if request.method == 'POST':
        if form.validate_on_submit():
            event.title = form.title.data
            event.date = form.date.data
            event.location = form.location.data
            event.description = form.description.data
            # event.category_id = form.category.data # Uncomment when category field is available

            db.session.commit()
            flash('Event updated successfully!')
            return redirect(url_for('events.get_event_form', event_id=event.id))

    return render_template('event_form.html', form=form, event=event)

@events_bp.route('/events', methods=['GET'])
def list_events_form():
    """Lists all events."""
    events = Event.query.all()
    return render_template('event_list.html', events=events)


@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event_form(event_id):
    """Get event details."""
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event)


@events_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event_form(event_id):
    """Delete an event."""
    event = Event.query.get_or_404(event_id)

    # Check if current user is the organizer of the event
    if event.organizer_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('events.list_events_form'))

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!')
    return redirect(url_for('events.list_events_form'))

@events_bp.route('/events/<int:event_id>/rsvp', methods=['POST'])
@login_required
def rsvp_event_form(event_id):
    """RSVP to an event."""
    event = Event.query.get_or_404(event_id)
    attendee = Attendee.query.filter_by(user_id=current_user.id).first()

    if not attendee:
        flash('User is not an attendee')
        return redirect(url_for('events.get_event_form', event_id=event_id))

    existing_rsvp = RSVP.query.filter_by(attendee_id=attendee.id, event_id=event_id).first()
    if existing_rsvp:
        flash('Already RSVPed')
        return redirect(url_for('events.get_event_form', event_id=event_id))

    rsvp = RSVP(attendee_id=attendee.id, event_id=event_id)
    db.session.add(rsvp)
    db.session.commit()
    flash('RSVP recorded')
    return redirect(url_for('events.get_event_form', event_id=event_id))
