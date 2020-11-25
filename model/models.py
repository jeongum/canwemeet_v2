# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Emotion(db.Model):
    __tablename__ = 'emotion'

    emotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emotion_name = db.Column(db.String(255), nullable=False)



class Highlight(db.Model):
    __tablename__ = 'highlight'

    highlight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    stt_id = db.Column(db.ForeignKey('realtime_STT.stt_id'), nullable=False, index=True)

    room = db.relationship('MeetingInformation', primaryjoin='Highlight.room_id == MeetingInformation.room_id', backref='highlights')
    stt = db.relationship('RealtimeSTT', primaryjoin='Highlight.stt_id == RealtimeSTT.stt_id', backref='highlights')
    user = db.relationship('User', primaryjoin='Highlight.user_id == User.user_id', backref='highlights')



class MeetingInformation(db.Model):
    __tablename__ = 'meeting_information'

    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    end_time = db.Column(db.DateTime)
    recode = db.Column(db.String(255), nullable=False)



class MeetingParticipant(db.Model):
    __tablename__ = 'meeting_participants'

    mp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    organizer = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    room = db.relationship('MeetingInformation', primaryjoin='MeetingParticipant.room_id == MeetingInformation.room_id', backref='meeting_participants')
    user = db.relationship('User', primaryjoin='MeetingParticipant.user_id == User.user_id', backref='meeting_participants')



class Memo(db.Model):
    __tablename__ = 'memo'

    memo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    room = db.relationship('MeetingInformation', primaryjoin='Memo.room_id == MeetingInformation.room_id', backref='memos')
    user = db.relationship('User', primaryjoin='Memo.user_id == User.user_id', backref='memos')



class RealtimeSTT(db.Model):
    __tablename__ = 'realtime_STT'

    stt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)
    time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False, index=True)
    content = db.Column(db.String, nullable=False)

    room = db.relationship('MeetingInformation', primaryjoin='RealtimeSTT.room_id == MeetingInformation.room_id', backref='realtime_stts')
    user = db.relationship('User', primaryjoin='RealtimeSTT.user_id == User.user_id', backref='realtime_stts')



class RealtimeEmotion(db.Model):
    __tablename__ = 'realtime_emotion'

    r_emotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)
    stt_id = db.Column(db.ForeignKey('realtime_STT.stt_id'), nullable=False, index=True)
    emotion_id = db.Column(db.ForeignKey('emotion.emotion_id'), nullable=False, index=True)

    emotion = db.relationship('Emotion', primaryjoin='RealtimeEmotion.emotion_id == Emotion.emotion_id', backref='realtime_emotions')
    room = db.relationship('MeetingInformation', primaryjoin='RealtimeEmotion.room_id == MeetingInformation.room_id', backref='realtime_emotions')
    stt = db.relationship('RealtimeSTT', primaryjoin='RealtimeEmotion.stt_id == RealtimeSTT.stt_id', backref='realtime_emotions')



class RealtimeMood(db.Model):
    __tablename__ = 'realtime_mood'

    mood_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mood_start_time = db.Column(db.DateTime, nullable=False)
    emotion_id = db.Column(db.ForeignKey('emotion.emotion_id'), nullable=False, index=True)
    room_id = db.Column(db.ForeignKey('meeting_information.room_id'), nullable=False, index=True)

    emotion = db.relationship('Emotion', primaryjoin='RealtimeMood.emotion_id == Emotion.emotion_id', backref='realtime_moods')
    room = db.relationship('MeetingInformation', primaryjoin='RealtimeMood.room_id == MeetingInformation.room_id', backref='realtime_moods')



class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255,'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    user_email = db.Column(db.String(255,'utf8mb4_unicode_ci'), nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
