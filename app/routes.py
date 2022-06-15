from flask import Flask, flash,render_template,request,redirect,url_for,session
from urllib.parse import parse_qs
import urllib.parse as urlparse

from sqlalchemy import true
from app import app,bcrypt,db
import requests
# from forms import RegisterForm
from models import User
import json

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']
        # 找碴資料庫USER是否存在
        user=User.query.filter_by(username=user).first()
        # 判斷帳號密碼是否輸入正確
        if user and bcrypt.check_password_hash(user.password,password):
            print('登入成功',user.username)
            
            session['user'] = user.username
            return redirect(url_for('user'))
        else:
            print('登入失敗')
            return render_template('login.html',login_state='登入失敗')
    return render_template('login.html')


@app.route('/user')
def user():
    if "user" in session:
        user=session['user']
        return render_template('user.html',user=user)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))


@app.route('/register',methods=['POST','GET'])
def register():
    front_end_data={'UserNameText':''}
    if request.method == 'POST':
        # username = request.form['username']
        # parsed = urlparse.urlparse(request.url)
        # groupQuery = 'username' in parse_qs(parsed.query)
        # print(groupQuery)
        if True:
            front_end_data['UserNameText']='username'
            user=request.form['user']
            password=request.form['password']
            print(user,password)
            # 有重複user處理
            if User.query.filter_by(username=user).first():
                print("重複user")
            else:
                # 對密碼加密(hash)
                password=bcrypt.generate_password_hash(password).decode('utf-8')
                user=User(username=user,password=password)
                db.session.add(user)
                db.session.commit()
                print("恭喜註冊成功")
                return redirect(url_for('login'))
    
    print('88888')
    return render_template('register.html',UserNameText=front_end_data['UserNameText'])

@app.route('/line_notify',methods=['POST','GET'])
def line_notify():
    tokenState=User.query.filter(User.username==session['user']).first().NotifyToken
    print(tokenState)
   
    return render_template('line_notify.html',tokenState=str(tokenState))


@app.route('/line_notify_bind',methods=['POST','GET'])
def line_notify_bind():
    notify_code=request.args.get('code')
    print(notify_code)
    # step1:https://notify-bot.line.me/zh_TW/
    # step2:到管理登入服務更改下面client_id,client_secret
    body = {
        "grant_type": "authorization_code",
        "code": notify_code,
        "redirect_uri": 'http://10.10.10.126:5000/line_notify_bind',
        "client_id": 'damgGNEOW7TW6vBtxoCWtt',
        "client_secret": 'ZWgOQ9CnOof0FHQNrvHhtTqAvjhBzHfecyELDWPSTqz'
    }
    user_token = requests.post("https://notify-bot.line.me/oauth/token", data=body)
    user_token=str(user_token.json()["access_token"])
    print('使用者token:'+user_token)
    User.query.filter_by(username=session['user']).update({'NotifyToken':user_token})
    db.session.commit()
    headers = {
    "Authorization": "Bearer "+user_token,
    "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
                'message': '第一次連動',
                'stickerId':'1993',
                'stickerPackageId':'446'}
    msg = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    print(msg) 
    return redirect(url_for('line_notify'))
   

@app.route('/line_notify_test',methods=['POST','GET'])
def line_notify_test():
    user_token=User.query.filter(User.username==session['user']).first().NotifyToken
    headers = {
        "Authorization": "Bearer "+user_token,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    msg = requests.get("https://notify-api.line.me/api/status", headers=headers)
    line_tokenState=str(msg.json()["message"])
    if line_tokenState=='ok':
        msg=requests.post("https://notify-api.line.me/api/revoke", headers=headers)
        User.query.filter_by(username=session['user']).update({'NotifyToken':'None'})
        db.session.commit()
        print(msg.json()["message"])
        print('1234')
        return redirect(url_for('line_notify'))

       
   