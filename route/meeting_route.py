import os
import re
import sys
from six.moves import queue
from flask import Flask, render_template, request, abort, Blueprint, url_for, session, jsonify
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, IpMessagingGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException
from model import models as minutedb

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

@meeting_route.route('/meeting', methods=['POST'])
def meeting_index():
    if 'roomname' in request.form:
        roomname = request.form['roomname']

    if 'username' in request.form:
        username = request.form['username']
    result = minutedb.db.engine.execute("SELECT user_name FROM user WHERE user_name=%s", (username))
                
    return render_template('meeting/index.html', roomname=roomname, username=username, result=result)


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


@meeting_route.route('/minute', methods=['GET','POST'])
def minute_list():
    name = request.form.get('submitname')    
    print(name)
    result = minutedb.db.engine.execute("SELECT * from meeting_participants AS mp INNER JOIN meeting_information AS mi INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_name =%s", (name))
    return render_template('minute/list.html', result=result)
