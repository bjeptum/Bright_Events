import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    assert response.status_code == 302  # Redirect after registration
    user = User.query.filter_by(username='testuser').first()
    assert user is not None

def test_login(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    })
    assert response.status_code == 302  # Redirect after login
    assert b'You have been logged in!' in response.data

def test_logout(client):
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
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect after logout
