import pytest
from app import create_app, db
from app.models import User, Event

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_event(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    })
    response = client.post('/events/create', data={
        'title': 'Test Event',
        'date': '2024-09-01',
        'location': 'Test Location',
        'category': 'Test Category'
    })
    assert response.status_code == 302  # Redirect after event creation
    event = Event.query.filter_by(title='Test Event').first()
    assert event is not None

def test_view_event(client):
    event = Event(title='Test Event', date='2024-09-01', location='Test Location', category='Test Category')
    db.session.add(event)
    db.session.commit()
    response = client.get(f'/events/{event.id}')
    assert response.status_code == 200
    assert b'Test Event' in response.data

def test_update_event(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    })
    event = Event(title='Test Event', date='2024-09-01', location='Test Location', category='Test Category')
    db.session.add(event)
    db.session.commit()
    response = client.post(f'/events/{event.id}/edit', data={
        'title': 'Updated Event',
        'date': '2024-09-02',
        'location': 'Updated Location',
        'category': 'Updated Category'
    })
    assert response.status_code == 302  # Redirect after event update
    updated_event = Event.query.filter_by(title='Updated Event').first()
    assert updated_event is not None

def test_delete_event(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    })
    event = Event(title='Test Event', date='2024-09-01', location='Test Location', category='Test Category')
    db.session.add(event)
    db.session.commit()
    response = client.post(f'/events/{event.id}/delete')
    assert response.status_code == 302  # Redirect after event deletion
    deleted_event = Event.query.filter_by(title='Test Event').first()
    assert deleted_event is None

