import os
import re
import sys
import time
import pyaudio
import json
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import types
from six.moves import queue
from flask import Flask, render_template, request, abort, Blueprint, url_for, session, jsonify
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, IpMessagingGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException

meeting_route = Blueprint('meeting_route',__name__)

twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

try:
    twilio_client = Client()
except TwilioException:
    twilio_client = None

def get_chatroom(name):
    for conversation in twilio_client.conversations.conversations.list():
        if conversation.friendly_name == name:
            return conversation

    # a conversation with the given name does not exist ==> create a new one
    return twilio_client.conversations.conversations.create(friendly_name=name)

class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

class SpeechClientBridge:
    def __init__(self):
        self._queue = queue.Queue()
        self._ended = False

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

        client = speech.SpeechClient()
        responses = client.streaming_recognize(
            streaming_config, 
            self.get_requests()
        )
        self.process_responses(responses)

    def terminate(self):
        self._ended = True

    def add_request(self, buffer):
        self._queue.put(types.StreamingRecognizeRequest(audio_content=bytes(buffer)))

    def get_requests(self):
        while not self._ended:
            yield self._queue.get()

    def process_responses(self, responses):
        thread = Thread(target=self.process_responses_loop, args=[responses])
        thread.start()

    def process_responses_loop(self, responses):
        for response in responses:
            self.on_response(response)
            if self._ended:
              break

    def on_response(self, response):
        if not response.results:
            return
        result = response.results[0]
        if not result.alternatives:
            return
        transcript = result.alternatives[0].transcript
        now = datetime.datetime.now()
        current_time = now.strftime('%A, %d %B %Y %H:%M:%S')
        print(current_time + ": "+transcript+"\n")


@meeting_route.route('/meeting')
def meeting_index():
    return render_template('meeting/index.html')

@meeting_route.route('/enter', methods=['POST'])
def enter():
    username = request.get_json(force=True).get('username')
    roomname = request.get_json(force=True).get('roomname')
    if not username:
        abort(401)

    conversation = get_chatroom(os.environ.get('CHATROOM', roomname))
    conversation_sid = ''
    if conversation:
        try:
            conversation.participants.create(identity=username)
        except TwilioRestException as ex:
            # do not error if the user is already in the conversation
            if ex.status != 409:
                raise
        conversation_sid = conversation.sid

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room=roomname))
    if conversation:
        token.add_grant(IpMessagingGrant(
            service_sid=conversation.chat_service_sid))

    return {'token': token.to_jwt().decode(),
            'conversation_sid': conversation_sid}
