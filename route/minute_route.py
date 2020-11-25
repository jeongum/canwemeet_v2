import os
from flask import Flask, render_template, request, Blueprint
from model import models as minutedb


minute_route = Blueprint('minute_route',__name__)

@minute_route.route('/minute')
def minute_list():
    minute = minutedb.MeetingInformation.query.all()
    
    return render_template('minute/list.html', minute=minute)

# Testing URL
@minute_route.route('/minute/details')
def minute_details():
    return render_template('minute/details.html')