import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy, create_engine, text
from flask_login import LoginManager
from dotenv import load_dotenv

from route.login_route import login_route
from route.meeting_route import meeting_route
from route.minute_route import minute_route

from config import DB_URL
import requests
import json
from oauth2client.contrib.flask_util import UserOAuth2

load_dotenv()

app = Flask(__name__)
app.secret_key = 'canwemeet'

#db info setting
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db set
db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(login_route)
app.register_blueprint(meeting_route)
app.register_blueprint(minute_route)



# kakao
@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    resToken = getAccessToken("db3901148da54e8931540503043c6259",str(code))  #XXXXXXXXX 자리에 RESET API KEY값을 사용
    return 'code=' + str(code) + '<br/>response for token=' + str(resToken)

def getAccessToken(clientId, code) :  # 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + clientId
    payload += "&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
    }
    reponse = requests.request("POST",url,data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token
    #return render_template('main.html')


# google
#app.config['SECRET_KEY'] = 'amumunjayeol'
#app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = 'client_secret_646888679664-jl0vefi6uljn4137itm4tb1vbumjoaf4.apps.googleusercontent.com.json'
#app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '646888679664-jl0vefi6uljn4137itm4tb1vbumjoaf4.apps.googleusercontent.com'
#app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = 'SixYOgpnu-pTvlRNXcVCMfhO'
#oauth2 = UserOAuth2(app)


# db
def create_app(test_config = None):
     app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:		# 2)
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database     = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)		# 3)
    app.database = database		# 4)
    
    return app		# 5)



if __name__ == '__main__':
    app.run(host='127.0.0.1',debug =True)
    