import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

from route.login_route import login_route
from route.meeting_route import meeting_route
<<<<<<< Updated upstream
from route.minute_route import minute_route
=======
from route.ser_route import ser_route
from config import DB_URL
import requests
import json
from oauth2client.contrib.flask_util import UserOAuth2
>>>>>>> Stashed changes

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
app.register_blueprint(meeting_route)
app.register_blueprint(minute_route)
<<<<<<< Updated upstream

=======
app.register_blueprint(ser_route)
 
@socketio.on('before_meeting', namespace='/meetingroom')
def before_meeting():
    print("===START STT===\n")
    emit('ready', broadcast='True')

@socketio.on('after_meeting', namespace='/meetingroom')
def after_meeting():
    print("===END STT===\n")
    emit('end', broadcast='True')
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug =True)
    