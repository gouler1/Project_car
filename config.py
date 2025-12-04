import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'  # Замени на реальный
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
