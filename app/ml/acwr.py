from datetime import datetime, timedelta
import pandas as pd
from app import db
from app.models import WorkoutLog

class ACWRCalculator:
    @staticmethod
    def calc_acwr(athlete_id):
        # get last 28 days of workout logs for the athlete
        today = datetime.now().date()
        start_date = today - timedelta(days=28)

        # get workout logs from the database
        workout_logs = WorkoutLog.query.filter(
            WorkoutLog.athlete_id == athlete_id,
            WorkoutLog.date >= start_date,
            WorkoutLog.date <= today
        ).all()

        if not workout_logs:
            return 0.0, 0.0, 1.0, "Low"
        
        # create a DataFrame from the workout logs
        data = [{
            'date': pd.to_datetime(log.date),
            'training_load': log.training_load
        } for log in workout_logs]

        df = pd.DataFrame(data)

        #group by date to get multiple logs per day
        df = df.groupby('date').sum().reset_index()

        #reset index to include all 28 days even if there are no logs for some days
        all_dates = pd.date_range(start=start_date, end=today)
        df = df.set_index('date').reindex(all_dates, fill_value=0).reset_index()
        df.rename(columns={'index': 'date'}, inplace=True)

        # calculate acute load of last 7 rows
        acute_load = df.tail(7)['training_load'].sum()
        avg_acute_load = acute_load / 7

        #chronic load of last 28 rows
        chronic_load = df.tail(28)['training_load'].sum()
        avg_chronic_load = chronic_load / 28

        # divition by zero check
        if avg_chronic_load == 0:
            acwr = 1.0
        else:
            acwr = avg_acute_load / avg_chronic_load


        risk_level = ACWRCalculator.get_risk_level(acwr)

        return round(avg_acute_load, 1), round(avg_chronic_load, 1), round(acwr, 2), risk_level
    

    @staticmethod
    def get_risk_level(ratio):
        if ratio <= 0.8:
            return "Low"
        elif 0.8 <= ratio <= 1.3:
            return "Optimal"
        elif 1.3 <= ratio <= 1.5:
            return "Moderate"
        else:
            return "High"
        