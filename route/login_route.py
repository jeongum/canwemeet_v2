import os
from flask import Flask,url_for, redirect, render_template, request,  Blueprint, session, jsonify
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from model import user_model as user
from config import DB_URL

login_route = Blueprint('login_route',__name__)

db = SQLAlchemy()

@login_route.route('/', methods=['GET','POST'])
def home():
    """ Session Control """
    '''if not session.get('logged_in'):
        return render_template('main.html')
    else:'''
    if request.method =='GET':
        username = request.form.get('gname', False)    
        email = request.form.get('gemail', False)
        return render_template('main.html')
        #return render_template('main.html')

'''
@login_route.route('/login',methods =['GET','POST'])
def login():
    """Login Form"""
    print()
    if request.method =='POST':
        return render_template('main.html')
    else:
        email = request.form['gemail']
        try:
            data = user.User.query.filter_by(user_email=email).first()
            if data is not None:
                session['logged_in'] = True
                return render_template('login/main.html')
            else:
                return 'Dont Login'
        except:
            return 'Dont Login'
'''
@login_route.route('/register/',methods =['GET','POST'])
def register():
    """Register Form"""
    if request.method =='POST':
        data = user.User(user_name = request.form['user_name'],user_email=request.form['user_email'])
        user.db.session.add(data)
        user.db.session.commit()
        return render_template('login/login.html')
    return render_template('login/register.html')

@login_route.route('/logout')
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('login_route.home'))

@login_route.route('/main')
def main():
    return render_template('main.html')

