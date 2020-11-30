import os
from flask import Flask, url_for, redirect, render_template, request,  Blueprint, session, jsonify
from flask_login import login_user

from model import models as user
from selenium import webdriver

login_route = Blueprint('login_route',__name__)

@login_route.route('/', methods=['GET','POST'])
def home():
    if  request.method == 'GET':
        return render_template('login/login.html')
    else:
        name = request.form.get('user_name', False)     
        try:    
            data = user.User.query.filter_by(user_name=name).first()
            print(data)
            if data is not None: # 데이터가 있으면
                session['logged_in'] = True
                result = user.db.engine.execute("SELECT user_name FROM user WHERE user_name=%s", (name))
                print(name)
                return render_template('main.html', result=result)
            else: 
                return render_template('login/login.html')
        except: # 예외입니다
            return render_template('main.html')


@login_route.route('/main')
def main():
    return render_template('main.html')