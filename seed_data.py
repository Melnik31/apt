import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, WorkoutLog, WellnessLog, AthleteProfile
from werkzeug.security import generate_password_hash

# Initialize the Flask App context explicitly for the file script
app = create_app()

with app.app_context():

    db.create_all()

    # Clear previous histories so the calculations remain clean
    WellnessLog.query.delete()
    WorkoutLog.query.delete()
    AthleteProfile.query.delete()
    User.query.delete()
    db.session.commit()

    # Create coach
    coach = User(
        username='coach1',
        email='coach1@mail.com',
        password_hash=generate_password_hash('password'),
        role='coach'
    )
    db.session.add(coach)
    db.session.commit()
    print(f'Coach created: {coach.username}')   
        

    #create multiple athletes with profiles, workout logs, and wellness logs
    #using list to store the data for each athlete and then loop through it to create the records in the database
    athletes_data = [
        {
            'username': 'Alex M',
            'email': 'alex@mail.com',
            'sport': 'Basketball',
            'position': 'Guard',
            'age': 25,
            'risk_profile': 'low'
        },
        {
            'username': 'John T',
            'email': 'john@mail.com',
            'sport': 'Football',
            'position': 'QB',
            'age': 20,
            'risk_profile': 'high'
        },
        {
            'username': 'Abby T',
            'email': 'abby@mail.com',
            'sport': 'volleyball',
            'position': 'center',
            'age': 27,
            'risk_profile': 'optimal'
        },
        {
            'username': 'Sam R',
            'email': 'sam@demo.com',
            'sport': 'Track',
            'position': 'Sprinter',
            'age': 21,
            'risk_profile': 'high'
        },
        {
            'username': 'Taylor K',
            'email': 'taylor@demo.com',
            'sport': 'Swimming',
            'position': 'Freestyle',
            'age': 19,
            'risk_profile': 'moderate'
        },
    ]

    #loop through to create records
    for data in athletes_data:
        #create user
        athlete = User(
            username=data['username'],
            email = data['email'],
            password_hash = generate_password_hash('password'),
            role = 'athlete'
        )
        db.session.add(athlete)
        db.session.commit()

        # Create AthleteProfile
        profile = AthleteProfile(
            user_id=athlete.id,
            coach_id=coach.id,
            sport=data['sport'],
            position=data['position'],
            age=data['age']
        )
        db.session.add(profile)
        db.session.commit()

        # Generate workout logs based on risk_profile
        for days_ago in range(27, -1, -1):
            if data['risk_profile'] == 'low':
                if days_ago > 7:
                    intensity = random.randint(5, 7)
                    duration = random.randint(45, 60)
                else:
                    intensity = random.randint(1, 2)
                    duration = random.randint(10, 15)
            elif data['risk_profile'] == 'optimal':
                intensity = random.randint(5, 7)
                duration = random.randint(45, 60)
            elif data['risk_profile'] == 'moderate':
                intensity = random.randint(4, 5) if days_ago > 14 else random.randint(7, 9)
                duration = random.randint(40, 50) if days_ago > 14 else random.randint(65, 80)
            else:  # high
                intensity = random.randint(2, 4) if days_ago > 7 else random.randint(8, 10)
                duration = random.randint(20, 30) if days_ago > 7 else random.randint(70, 90)

            log = WorkoutLog(
                athlete_id=athlete.id,
                date=datetime.now() - timedelta(days=days_ago),
                workout_type=random.choice(['Strength', 'Cardio', 'Sport-specific']),
                duration_minutes=duration,
                intensity=intensity,
                notes='test Data'
            )
            db.session.add(log)

        # Generate wellness logs
        for days_ago in range(27, -1, -1):
            wellness = WellnessLog(
                athlete_id=athlete.id,
                date=datetime.now() - timedelta(days=days_ago),
                sleep_hours=round(random.uniform(6.0, 9.0), 1),
                soreness=random.randint(1, 5),
                mood=random.randint(6, 10),
                resting_heart_rate=random.randint(55, 70)
            )
            db.session.add(wellness)

        db.session.commit()
        print(f"Created athlete: {data['username']}")