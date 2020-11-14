import os
from flask import Flask, render_template, request, Blueprint

meeting_route = Blueprint('meeting_route',__name__)

@meeting_route.route('/meeting')
def meeting_index():
    return render_template('meeting/index.html')