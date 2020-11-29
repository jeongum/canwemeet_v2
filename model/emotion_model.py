
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Emotion(db.Model):
    """ 
    
    """
    __tablename__ = 'emotion'

    emotion_id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement=True)
    emotion_name = db.Column(db.String(255,'utf8mb4_unicode_ci'))

    def  __init__(self, emotion_name):
        self.emotion_name = emotion_name
