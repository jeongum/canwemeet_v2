import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

from route.login_route import login_route
from route.chat_route import chat_route
from route.stt_route import stt_route
from route.meeting_route import meeting_route
from route.minute_route import minute_route

from config import DB_URL

load_dotenv()

app = Flask(__name__)
app.secret_key = 'canwemeet'

#db info setting
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db set
db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(login_route)
app.register_blueprint(chat_route)
app.register_blueprint(stt_route)
app.register_blueprint(meeting_route)
app.register_blueprint(minute_route)

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug =True)
    