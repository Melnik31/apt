# configuration for the Flask application
class Config:
    SECRET_KEY = "melnik"
    SQLALCHEMY_DATABASE_URI = "sqlite:///perform_tracker.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False