import os
from flask import Flask, url_for, redirect, render_template, request,  Blueprint, session, jsonify
from flask_login import login_user

from model import models as user

login_route = Blueprint('login_route',__name__)

loginAuth = 1
@login_route.route('/', methods=['GET','POST'])
def home():
    global loginAuth
    """ Session Control """
    if  not session.get('logged_in') and loginAuth == 2: # 로그인 처리
        name = request.form.get('user_name', False)    
        email = request.form.get('user_email', False)   
        try:    
            data = user.User.query.filter_by(user_name=name, user_email=email).first()
            if data is not None: # 데이터가 있으면
                session['logged_in'] = True
                loginAuth = 3
                print(loginAuth)
                return render_template('main.html')
            else: # 데이터가 없으면 -> 회원가입 처리
                print("dbpage")
                data = user.User(user_name = request.form['user_name'],user_email=request.form['user_email'])
                user.db.session.add(data)
                user.db.session.commit()
                session['logged_in'] = True
                return render_template('main.html')
        except: # 예외입니다
            return render_template('login/login.html')
       
    elif session.get('logged_in'): # 로그인 세션이 있을 경우
        return render_template('main.html')

    else: # 로그인 세션이 없는 경우
        print("loginAuth")
        loginAuth = 2
        return render_template('login/login.html')

'''
@login_route.route('/login',methods =['GET','POST'])
def login():
    global loginAuth
    """ Session Control """
    if  not session.get('logged_in') and loginAuth == 2: # 로그인 처리
        name = request.form.get('user_name', False)    
        email = request.form.get('user_email', False)   
        try:    
            data = user.User.query.filter_by(user_name =name, user_email=email).first()
            if data is not None: # 데이터가 있으면
                session['logged_in'] = True
                loginAuth = 3
                print(loginAuth)
                return render_template('main.html')
            else: # 데이터가 없으면 -> 회원가입 처리
                data = user.User(user_name = request.form['user_name'],user_email=request.form['user_email'])
                user.db.session.add(data)
                user.db.session.commit()
                render_template('login/main.html')
        except: # 예외입니다
            render_template('login/login.html')
       
    elif session.get('logged_in'): # 로그인 세션이 있을 경우
        render_template('main.html')
    else: # 로그인 세션이 없는 경우
        print("loginAuth")
        loginAuth = 2
        return render_template('login/login.html')


@login_route.route('/logout')
def logout():
    """Logout Form"""
    global loginAuth
    loginAuth = 1
    session['logged_in'] = False
    session.clear()
    #return redirect(url_for('login_route.login'))
    return render_template('login/logout.html')
'''
@login_route.route('/main')
def main():
    return render_template('main.html')