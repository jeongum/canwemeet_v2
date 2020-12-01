import os
from flask import Flask, render_template, request, Blueprint, url_for, redirect, session, jsonify
from model import models as minutedb


minute_route = Blueprint('minute_route',__name__)
'''
@minute_route.route('/minute')
def minute_list():
    minute = minutedb.MeetingInformation.query.filter().all()
    result = minutedb.db.engine.execute("SELECT * from meeting_participants AS mp INNER JOIN meeting_information AS mi INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_name = '윤소현'")
    return render_template('minute/list.html', result=result)
'''
@minute_route.route('/minute', methods=['POST'])
def minute_list():
    name = request.form.get('name1')    
    print(name)
    result = minutedb.db.engine.execute("SELECT mi.room_id, mi.start_time, mi.room_title, mi.recode from meeting_participants AS mp INNER JOIN meeting_information AS mi INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_name = %s ORDER BY mi.room_id", (name))
    return render_template('minute/list.html', result=result)

# Testing URL
@minute_route.route('/minute/details', methods=['GET'])
def minute_details():
    board_id = request.args.get("mid")
    print(board_id)
    name = request.args.get('subname') 
    print(name)
    result = minutedb.db.engine.execute("SELECT room_title, DATE(start_time) AS date, TIME(start_time) AS ST, TIME(end_time) AS ET from meeting_information AS mi WHERE mi.room_id =%s", (board_id))
    usernum = minutedb.db.engine.execute("SELECT count(us.user_name) AS unum from meeting_information AS mi INNER JOIN meeting_participants AS mp INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE mi.room_id=%s", (board_id))
    name1 = minutedb.db.engine.execute("SELECT us.user_name from meeting_information AS mi INNER JOIN meeting_participants AS mp INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_id=1 AND mi.room_id=%s", (board_id))
    name2 = minutedb.db.engine.execute("SELECT us.user_name from meeting_information AS mi INNER JOIN meeting_participants AS mp INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_id=2 AND mi.room_id=%s", (board_id))
    name3 = minutedb.db.engine.execute("SELECT us.user_name from meeting_information AS mi INNER JOIN meeting_participants AS mp INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_id=3 AND mi.room_id=%s", (board_id))
    name4 = minutedb.db.engine.execute("SELECT us.user_name from meeting_information AS mi INNER JOIN meeting_participants AS mp INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_id=4 AND mi.room_id=%s", (board_id))
    memo = minutedb.db.engine.execute("SELECT content, memo_id FROM memo INNER JOIN user ON memo.user_id = user.user_id WHERE user.user_name = '윤소현' AND memo.room_id = %s", (board_id))
    stt = minutedb.db.engine.execute("SELECT hour(rstt.time) AS hour, minute(rstt.time) AS minute, rstt.content, em.emotion_name, user.user_name FROM realtime_STT as rstt INNER JOIN user ON rstt.user_id=user.user_id inner join realtime_mood as rm on rstt.stt_id = rm.stt_id inner join emotion as em on rm.emotion_id = em.emotion_id where rstt.room_id = %s ORDER BY rstt.stt_id", (board_id))
    
    return render_template('minute/details.html', result=result, usernum=usernum, name1=name1, name2=name2, name3=name3, name4=name4, stt=stt, memo=memo)


@minute_route.route('/minute/details/memo', methods=['GET'])
def minute_update():   
    return render_template('main.html')
