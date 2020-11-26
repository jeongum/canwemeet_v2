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
@minute_route.route('/minute', methods=['GET','POST'])
def minute_list():
    name = request.form.get('submitname')    
    print(name)
    result = minutedb.db.engine.execute("SELECT * from meeting_participants AS mp INNER JOIN meeting_information AS mi INNER JOIN user AS us ON mp.room_id = mi.room_id AND mp.user_id = us.user_id WHERE us.user_name =%s", (name))
    return render_template('minute/list.html', result=result)

# Testing URL
@minute_route.route('/minute/details')
def minute_details():
    return render_template('minute/details.html')