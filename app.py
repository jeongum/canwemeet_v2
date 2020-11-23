import os
import base64
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import eventlet
from dotenv import load_dotenv
from route.login_route import login_route
from route.minute_route import minute_route
from route.meeting_route import meeting_route, MicrophoneStream
from google.cloud import speech_v1 as speech
from config import DB_URL

load_dotenv()

app = Flask(__name__)
app.secret_key = 'canwemeet'
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

EXIT_FLAG = True

@socketio.on('before_meeting', namespace='/myspace')
def before_meeting():
    global EXIT_FLAG
    EXIT_FLAG = not(EXIT_FLAG)
    print("===START STT===\n")
    eventlet.spawn(start_meeting)
    emit('ready')

@socketio.on('after_meeting', namespace='/myspace')
def after_meeting():
    global EXIT_FLAG
    EXIT_FLAG = not(EXIT_FLAG)
    print("===END STT===\n")

@socketio.on('start_meeting', namespace='/myspace')
def start_meeting():
    RATE = 16000
    CHUNK = int(RATE / 10 )
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
        # max_alternatives=1
        #audio_channel_count=2,    # The number of channels 
        #enable_separate_recognition_per_channel=True # audio_channel_count > 1 to get each channel recognized separately.
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config= config, interim_results=True
    )
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator)
        responses = client.streaming_recognize(
        streaming_config, requests)
        listen_loop(responses)

def listen_loop(responses):
    global EXIT_FLAG
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        if EXIT_FLAG:
            break
        if result.is_final:
            now = datetime.datetime.now()
            current_time = now.strftime('%A, %d %B %Y %H:%M:%S')
            print(current_time + ": "+transcript+"\n")
            

if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug =True)
    socketio.run(app, port=5000, debug=True)
