"""
Database Models for Wellness Hub
Using SQLAlchemy ORM for PostgreSQL
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model - for future authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    daily_logs = db.relationship('DailyLog', backref='user', lazy=True, cascade='all, delete-orphan')
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True, cascade='all, delete-orphan')

class JournalEntry(db.Model):
    """Journal entries with sentiment analysis"""
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    
    # Sentiment analysis fields
    sentiment = db.Column(db.String(20))  # positive, negative, neutral
    score = db.Column(db.Float)
    polarity = db.Column(db.Float)
    subjectivity = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.time.strftime('%H:%M'),
            'sentiment': self.sentiment,
            'score': self.score,
            'edited': self.edited_at.strftime('%Y-%m-%d %H:%M') if self.edited_at else None
        }

class DailyLog(db.Model):
    """Daily tracking logs for dashboard"""
    __tablename__ = 'daily_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    
    # Tracking metrics
    sleep_hours = db.Column(db.Float, nullable=False, default=0)
    mood_rating = db.Column(db.Float, nullable=False, default=5)
    study_hours = db.Column(db.Float, nullable=False, default=0)
    water_intake = db.Column(db.Integer, nullable=False, default=0)
    exercise_minutes = db.Column(db.Integer, nullable=False, default=0)
    productivity_score = db.Column(db.Integer, nullable=False, default=50)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'sleep_hours': float(self.sleep_hours),
            'mood_rating': float(self.mood_rating),
            'study_hours': float(self.study_hours),
            'water_intake': int(self.water_intake),
            'exercise_minutes': int(self.exercise_minutes),
            'productivity_score': int(self.productivity_score)
        }

class MealPlan(db.Model):
    """Saved meal plans"""
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # User profile data
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    activity_level = db.Column(db.String(20), nullable=False)
    goal = db.Column(db.String(20), nullable=False)
    restrictions = db.Column(db.JSON)
    
    # Calculated values
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)
    calorie_goal = db.Column(db.Integer)
    
    # Meal plan data (stored as JSON)
    meal_plan_data = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'goal': self.goal,
            'restrictions': self.restrictions,
            'bmi': self.bmi,
            'bmr': self.bmr,
            'calorie_goal': self.calorie_goal,
            'meal_plan_data': self.meal_plan_data,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }