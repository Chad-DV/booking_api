import uuid
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Booking(db.Model):
    room_id = db.Column(db.String(36), primary_key=True)
    booked_by = db.Column(db.String(100), nullable=False)
    booking_start = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    booking_end = db.Column(db.DateTime, nullable=False)

    def __init__(self, 
                 booked_by:str, 
                 booking_end:datetime | None,
                 booking_start:datetime = datetime.now(), 
                 duration_minutes:int = 60):
        self.room_id = str(uuid.uuid4())
        self.booked_by = booked_by
        self.booking_start = booking_start
        self.duration_minutes = duration_minutes
        self.booking_end = booking_end or booking_start + timedelta(minutes=self.duration_minutes)