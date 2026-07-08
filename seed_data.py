import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, WorkoutLog, WellnessLog

# Initialize the Flask App context explicitly for the file script
app = create_app()

with app.app_context():
    print("🧹 Targetting 'John Test' and removing old conflicting records...")
    athlete = User.query.filter_by(username='John Test').first()

    if athlete:
        # Clear previous histories so the calculations remain clean
        WorkoutLog.query.filter_by(athlete_id=athlete.id).delete()
        WellnessLog.query.filter_by(athlete_id=athlete.id).delete()
        db.session.commit()

        # Anchoring to July 6, 2026 to align with your dashboard view
        today = datetime(2026, 7, 6).date()

        print("📈 Generating a highly sustainable 28-day progressive training loop...")
        for i in range(28, -1, -1):
            log_date = today - timedelta(days=i)
            
            # Predictable 4-day training schedule every week
            if i % 7 in [1, 3, 5, 6]:
                duration = random.choice([45, 50])
                intensity = random.choice([4, 5])  # Moderate RPE exertion metrics
                
                workout = WorkoutLog(
                    athlete_id=athlete.id,
                    date=log_date,
                    workout_type=random.choice(['strength', 'cardio', 'sport']),
                    duration_minutes=duration,
                    intensity=intensity,
                    notes="Progressive base preparation session"
                )
                db.session.add(workout)
                
            # Consistent healthy sleep and standard physical adaptation indices
            wellness = WellnessLog(
                athlete_id=athlete.id,
                date=log_date,
                sleep_hours=random.choice([7.5, 8.0, 8.5]),
                soreness=random.choice([2, 3]),
                mood=random.choice([7, 8, 9]),
                resting_heart_rate=random.choice([56, 58, 60])
            )
            db.session.add(wellness)

        db.session.commit()
        print("🚀 Success! Balanced baseline training timeline successfully committed.")
    else:
        print("❌ Error: Could not find an athlete named 'John Test'")