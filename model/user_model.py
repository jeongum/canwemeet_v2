'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ Create user """
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement=True)
    user_name = db.Column(db.String(255,'utf8mb4_unicode_ci'))
    user_email = db.Column(db.String(255,'utf8mb4_unicode_ci'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.FetchedValue())

    def  __init__(self, user_name, user_email):
        self.user_name = user_name
        self.user_email = user_email
'''