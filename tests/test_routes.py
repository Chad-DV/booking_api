import pytest
from app.views import app
from app.models import Booking,db
from datetime import datetime
from flask_migrate import Migrate
from config import TestingConfig

app.config.from_object(TestingConfig)

db.init_app(app)
migrate = Migrate(app, db)


# create SQLite client for test
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# sucessfull status code 
def test_create_booking(client):
    response = client.post('/room_booking')
    assert response.status_code == 201

# sucessfull status code
def test_delete_booking(client):
    with app.app_context():
        booking = Booking(booked_by='Test User', booking_start=datetime.utcnow(), duration_minutes=60, booking_end=None)
        db.session.add(booking)
        db.session.commit()

        response = client.delete(f'/room_booking/{booking.room_id}')
        print("RESPONSE!! -> ", response.status)
        assert response.status_code == 202

# sucessfull status code
def test_get_booking(client):
    with app.app_context():
        booking = Booking(booked_by='Test User', booking_start=datetime.utcnow(), duration_minutes=60,booking_end=None)
        db.session.add(booking)
        db.session.commit()

        response = client.get(f'/room_booking/{booking.room_id}')
        assert response.status_code == 200

# sucessfull status code
def test_get_all_bookings(client):
    with app.app_context():
        bookings = [
            Booking(booked_by='User1', booking_start=datetime.utcnow(), duration_minutes=60, booking_end=None),
            Booking(booked_by='User2', booking_start=datetime.utcnow(), duration_minutes=120, booking_end=None)
        ]
        db.session.add_all(bookings)
        db.session.commit()

        response = client.get('/room_booking')
        assert response.status_code == 200

# sucessfull status code
def test_create_booking_with_params(client):
    with app.app_context():
        response = client.post('/room_booking/TestUser/2024-04-22T10:00:00/60')
        assert response.status_code == 201

# sucessfull status code
def test_edit_booking(client):
    with app.app_context():
        booking = Booking(booked_by='Test User', booking_start=datetime.utcnow(), duration_minutes=60, booking_end=None)
        db.session.add(booking)
        db.session.commit()

        response = client.put(f'/room_booking/{booking.room_id}/NewUser/2024-04-22T12:00:00/90')
        assert response.status_code == 201