import pytest
from app import create_app, db
from app.models import User, WorkoutLog
from werkzeug.security import generate_password_hash
from app.ml.acwr import ACWRCalculator

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_page_load(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_acwr_risk_levels():
    assert ACWRCalculator.get_risk_level(0.5) == 'Low'
    assert ACWRCalculator.get_risk_level(1.0) == 'Optimal'
    assert ACWRCalculator.get_risk_level(1.4) == 'Moderate'
    assert ACWRCalculator.get_risk_level(2.0) == 'High'


def test_dublicate_registretion(client, app):
    #register #1
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password',
        'role': 'athlete',
        'sport': 'Basketball',
        'position': 'Guard'
    }, follow_redirects = True)

    # register again with same username
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'different@test.com',
        'password': 'password',
        'role': 'athlete',
        'sport': 'Basketball',
        'position': 'Guard'
    }, follow_redirects=True)

    # Assert error message appears on page
    assert b'already exists' in response.data

def test_register_new_user(client,app):
    client.post('/register', data={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'password',
            'role': 'athlete',
            'sport': 'Basketball',
            'position': 'Guard'
        }, follow_redirects= True)

    with app.app_context():
        user = User.query.filter_by(username = 'testuser').first()
        assert user is not None
        assert user.role == 'athlete'

def test_wrong_password(client, app):
    #create test user
    with app.app_context():
        user = User(
            username='testuser',
            email='test@test.com',
            password_hash=generate_password_hash('password'),
            role='athlete' 
        )
        db.session.add(user)
        db.session.commit()

    #login with wrong pass
    response = client.post('/login', data={
        'username': 'testuser',
        'password' : 'wrongpass'
    }, follow_redirects = True)

    assert b'Invalid' in response.data




