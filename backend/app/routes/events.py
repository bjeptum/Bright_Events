from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import jsonify
from ..models import db, Event, RSVP, EventCategory, Organizer, Attendee
from flask_login import current_user, login_required
from flask_login import LoginManager
from ..forms import EventForm

events_bp = Blueprint('events', __name__)

# API Routes
@events_bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.get_json()
    title = data.get('title')
    date = data.get('date')
    location = data.get('location')
    category_id = data.get('category_id')
    
    if not title or not date or not location or not category_id:
        return jsonify({'error': 'Missing data'}), 400

    if not EventCategory.query.get(category_id):
        return jsonify({'error': 'Invalid category'}), 400

    event = Event(title=title, date=date, location=location, category_id=category_id, organizer_id=current_user.id)
    db.session.add(event)
    db.session.commit()
    return jsonify({'id': event.id}), 201

@events_bp.route('/api/events', methods=['GET'])
def list_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'date': event.date.isoformat(),
        'location': event.location,
        'category': event.category.name
    } for event in events])

@events_bp.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'date': event.date.isoformat(),
        'location': event.location,
        'category': event.category.name
    })

@events_bp.route('/api/events/<int:event_id>', methods=['POST'])
@login_required
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    event.title = data.get('title', event.title)
    event.date = data.get('date', event.date)
    event.location = data.get('location', event.location)
    event.category_id = data.get('category', event.category_id)
    
    db.session.commit()
    return jsonify({'message': 'Event updated'})

@events_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'})

@events_bp.route('/api/events/<int:event_id>/rsvp', methods=['POST'])
@login_required
def rsvp_event(event_id):
    event = Event.query.get_or_404(event_id)
    attendee = Attendee.query.filter_by(user_id=current_user.id).first()

    if not attendee:
        return jsonify({'error': 'User is not an attendee'}), 400

    existing_rsvp = RSVP.query.filter_by(attendee_id=attendee.id, event_id=event_id).first()
    if existing_rsvp:
        return jsonify({'error': 'Already RSVPed'}), 400

    rsvp = RSVP(attendee_id=attendee.id, event_id=event_id)
    db.session.add(rsvp)
    db.session.commit()
    return jsonify({'message': 'RSVP recorded'})

@events_bp.route('/api/events/<int:event_id>/rsvps', methods=['GET'])
def get_rsvps(event_id):
    event = Event.query.get_or_404(event_id)
    rsvps = RSVP.query.filter_by(event_id=event_id).all()
    return jsonify([{
        'user_id': RSVP.attendee_id,
        'username': RSVP.attendee.user.username
    } for RSVP in rsvps])

# HTML Form Requests
@events_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event_form():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            description=form.description.data,
            category_id=form.category.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('events.list_events_form'))
    else:
         print(form.errors)  # Debugging
    return render_template('event_form.html', form=form)

@events_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event_form(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('events.list_events_form'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.location = form.location.data
        event.description = form.description.data
        event.category_id = form.category.data

        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('events.list_events_form'))

    return render_template('event_form.html', form=form, event=event)

@events_bp.route('/events', methods=['GET'])
def list_events_form():
    events = Event.query.all()
    return render_template('events_list.html', events=events)
