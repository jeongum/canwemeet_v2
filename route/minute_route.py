import os
from flask import Flask, render_template, request, Blueprint

minute_route = Blueprint('minute_route',__name__)

@minute_route.route('/minute')
def minute_list():
    return render_template('minute/list.html')

# Testing URL
@minute_route.route('/minute/details')
def minute_details():
    return render_template('minute/details.html')