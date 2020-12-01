import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from route.login_route import login_route
from route.minute_route import minute_route
from route.meeting_route import meeting_route
from route.ser_route import ser_route
from config import DB_URL
import requests
import json
from oauth2client.contrib.flask_util import UserOAuth2

# Internal imports
#from user import User

load_dotenv()

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("646888679664-oklga1e16gl0c5fcniv49b039v7qs4ok.apps.googleusercontent.com", None)
GOOGLE_CLIENT_SECRET = os.environ.get("HsSzEOXBr67V4OgPIDiA_GKZ", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


#db info setting
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db set
db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(login_route)
app.register_blueprint(meeting_route)
app.register_blueprint(minute_route)
app.register_blueprint(ser_route)

@socketio.on('before_meeting', namespace='/meetingroom')
def before_meeting():
    print("===START STT===\n")
    emit('ready', broadcast='True')

@socketio.on('after_meeting', namespace='/meetingroom')
def after_meeting():
    print("===END STT===\n")
    emit('end', broadcast='True')

@socketio.on('send_message', namespace='/meetingroom')
def send_message(json):
    emit('receive_message', json, broadcast='True')
            
if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug =True)
    socketio.run(app, port=5000, debug=True)
