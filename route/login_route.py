import os
from flask import Flask,url_for, redirect, render_template, request,  Blueprint, session, jsonify
from flask_login import login_user

from model import user_model as user

login_route = Blueprint('login_route',__name__)


@login_route.route('/', methods=['GET','POST'])
def home():
    """ Session Control """
    if not session.get('logged_in'):
        return render_template('login/login.html')
    else:
        if request.method =='POST':
            username = request.form['user_name']
            return render_template('main.html')
        return render_template('main.html')
    
@login_route.route('/login',methods =['GET','POST'])
def login():
    """Login Form"""
    if request.method =='GET':
        return render_template('main.html')
    else:
        name = request.form['user_name']
        email = request.form['user_email']
        try:
            data = user.User.query.filter_by(user_name =name, user_email=email).first()
            if data is not None:
                session['logged_in'] = True
                return render_template('main.html')
            else:
                return 'Dont Login'
        except:
            return 'Dont Login'

@login_route.route('/register/',methods =['GET','POST'])
def register():
    """Register Form"""
    if request.method =='POST':
        data = user.User(user_name = request.form['user_name'],user_email=request.form['user_email'])
        user.db.session.add(data)
        user.db.session.commit()
        return render_template('main.html')
    return render_template('login/register.html')

@login_route.route('/logout')
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('login_route.home'))