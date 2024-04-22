from app.models import Booking,db
from flask import jsonify,Flask
from datetime import datetime
import uuid


app = Flask(__name__)

# Crete a booking (default)
@app.route('/room_booking', methods=['POST'])
def create_Booking():
    default_booking = Booking(booked_by='Default User',booking_end=None)
    db.session.add(default_booking)
    db.session.commit()

    return jsonify({'Booking create successfully': f'{default_booking.room_id}'}), 201

# Delete Booking
@app.route('/room_booking/<string:room_id>', methods=['DELETE'])
def delete_booking(room_id):
    try:
        room_uuid = str(uuid.UUID(room_id))
    except ValueError:
        return jsonify({'error': 'Invalid UUID string'}), 400

    booking = Booking.query.filter_by(room_id=room_uuid).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking deleted successfully'}),202


# Return Booking information
@app.route('/room_booking/<string:room_id>', methods=['GET'])
def get_booking(room_id):
    try:
        room_uuid = str(uuid.UUID(room_id))
    except ValueError:
        return jsonify({'error': 'Invalid UUID string'}), 400

    booking = Booking.query.filter_by(room_id=room_uuid).first()

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    booking_data = {
        'room_id': str(booking.room_id),
        'booked_by': booking.booked_by,
        'booking_start': booking.booking_start.isoformat(),
        'duration_minutes': booking.duration_minutes
    }

    return jsonify(booking_data),200

# Return Booking information for all bookings
@app.route('/room_booking', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    bookings_data = []
    
    for booking in bookings:
        booking_data = {
            'room_id': str(booking.room_id),
            'booked_by': booking.booked_by,
            'booking_start': booking.booking_start.isoformat(),
            'duration_minutes': booking.duration_minutes
        }
        bookings_data.append(booking_data)

    return jsonify(bookings_data), 200

# Create Booking -> TODO: Chage This to use a body for data instead of URL
@app.route('/room_booking/<booked_by>/<booking_start>/<int:duration_minutes>', methods=['POST'])
def create_booking(booked_by, booking_start, duration_minutes):
    try:
        booking_start = datetime.strptime(booking_start, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format for booking_start'}), 400

    room_id = str(uuid.uuid4())

    booking = Booking(
        booked_by=booked_by,
        booking_start=booking_start,
        duration_minutes=duration_minutes,
        booking_end=None
    )

    db.session.add(booking)
    db.session.commit()

    response_data = {
        'message': 'Booking created successfully',
        'booking': {
            'room_id': room_id,
            'booked_by': booked_by,
            'booking_start': booking_start.isoformat(),
            'duration_minutes': duration_minutes
        }
    }
    return jsonify(response_data), 201

# Update Booking -> TODO: Chage This to use a body for data instead of URL
@app.route('/room_booking/<string:room_id>/<string:booked_by>/<string:booking_start>/<int:duration_minutes>', methods=['PUT'])
def edit_booking(room_id, booked_by, booking_start, duration_minutes):
    booking = Booking.query.filter_by(room_id=room_id).first()

    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    booking.booked_by = booked_by
    try:
        booking_start = datetime.strptime(booking_start, '%Y-%m-%dT%H:%M:%S')
        booking.booking_start = booking_start
    except ValueError:
        return jsonify({'error': 'Invalid datetime format for booking_start'}), 400
    
    booking.duration_minutes = duration_minutes
    db.session.commit()

    response_data = {
        'message': 'Booking updated successfully',
        'booking': {
            'room_id': room_id,
            'booked_by': booked_by,
            'booking_start': booking_start.isoformat(),
            'duration_minutes': duration_minutes
        }
    }
    return jsonify(response_data),201