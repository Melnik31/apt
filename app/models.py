from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'coach' or 'athlete'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AthleteProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sport = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    injury_history = db.Column(db.Text, nullable=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Link to coach
    user = db.relationship('User', foreign_keys=[user_id], backref='athlete_profile')

class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)  # e.g., 1-10 scale
    notes = db.Column(db.Text, nullable=True)

    @property
    def training_load(self):
        # Example training load calculation (duration * intensity)
        return self.duration_minutes * self.intensity

class WellnessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    soreness = db.Column(db.Integer, nullable=False)  #1-10 scale
    mood = db.Column(db.Integer, nullable=False)  # 1-10 scale
    resting_heart_rate = db.Column(db.Integer, nullable=True)
    
