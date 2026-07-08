from datetime import datetime, timedelta
import pandas as pd
from app.models import WorkoutLog

class ACWRCalculator:
    @staticmethod
    def calc_acwr(athlete_id):
        start_date = datetime.now() - timedelta(days=28)
        today = datetime.now()

        workout_logs = WorkoutLog.query.filter(
            WorkoutLog.athlete_id == athlete_id,
            WorkoutLog.date >= start_date,
            WorkoutLog.date <= today
        ).all()

        if not workout_logs:
            return 0.0, 0.0, 1.0, "Low"

        data = [{
            'date': pd.to_datetime(log.date),
            'training_load': log.training_load
        } for log in workout_logs]

        df = pd.DataFrame(data)
        df = df.groupby('date').sum().reset_index()

        # Normalize BEFORE reindex
        df['date'] = df['date'].dt.normalize()
        all_dates = pd.date_range(start=start_date, end=today).normalize()

        df = df.set_index('date').reindex(all_dates, fill_value=0).reset_index()
        df.rename(columns={'index': 'date'}, inplace=True)

        acute_load = df.tail(7)['training_load'].sum()
        avg_acute_load = acute_load / 7

        chronic_load = df.tail(28)['training_load'].sum()
        avg_chronic_load = chronic_load / 28

        if avg_chronic_load == 0:
            acwr = 1.0
        else:
            acwr = avg_acute_load / avg_chronic_load

        risk_level = ACWRCalculator.get_risk_level(acwr)

        return round(avg_acute_load, 1), round(avg_chronic_load, 1), round(acwr, 2), risk_level

    @staticmethod
    def get_risk_level(ratio):
        if ratio < 0.8:
            return "Low"
        elif ratio <= 1.3:
            return "Optimal"
        elif ratio <= 1.5:
            return "Moderate"
        else:
            return "High"