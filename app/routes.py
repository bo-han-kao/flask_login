from array import array
from tkinter import N
from flask import Flask, flash,render_template,request,redirect,url_for,session as flask_session
from urllib.parse import parse_qs
import urllib.parse as urlparse

from sqlalchemy import join, table,text
from sqlalchemy.sql import select

from app import app,bcrypt,db
import requests
# from forms import RegisterForm
from models import User,Notify_status
import json


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    # 網址資訊
    parsed = urlparse.urlparse(request.url)
    # 看網址是否含LINE_UUID參數
    groupQuery = 'LINE_UUID' in parse_qs(parsed.query)
    print(groupQuery)
    if groupQuery == True:
        # 取得line_uuid
        line_uuid=parsed.query.split('=')[1]
        db_line_uuid=User.query.filter_by(Line_uuid=line_uuid).first()
        print(db_line_uuid)
        if str(db_line_uuid)=='None':
            print('沒有line id')
            return redirect(url_for('register',LINE_UUID=line_uuid))

    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']
        # 找碴資料庫USER是否存在
        user=User.query.filter_by(username=user).first()
        # 判斷帳號密碼是否輸入正確
        if user and bcrypt.check_password_hash(user.password,password):
            print('登入成功',user.username)
            flask_session['user'] = user.username
            return redirect(url_for('user'))
        else:
            print('登入失敗')
            return render_template('login.html',login_state='登入失敗')
    
    return render_template('login.html')


@app.route('/user')
def user():
    if "user" in flask_session:
        user=flask_session['user']
        return render_template('user.html',user=user)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    flask_session.pop('user',None)
    return redirect(url_for('login'))

#待修改
@app.route('/register',methods=['POST','GET'])
def register():
    # 網址資訊
    parsed = urlparse.urlparse(request.url)
    groupQuery = 'LINE_UUID' in parse_qs(parsed.query)
    line_uuid = False
    print(groupQuery)
    if groupQuery==True:
        line_uuid=parsed.query.split('=')[1]
    
    if request.method == 'POST':
        
        user=request.form['user']
        password=request.form['password']
        print(user,password,groupQuery)
        # 有重複user處理
        if User.query.filter_by(username=user).first():
            print(parsed)
            if line_uuid:
                return render_template('register.html',register_state='名稱已被註冊',line_uuid=line_uuid)

        else:
            # 對密碼加密(hash)
            password=bcrypt.generate_password_hash(password).decode('utf-8')
            if line_uuid:
                line_uuid=request.form['Line_uuid']
                user=User(username=user,password=password,Line_uuid=line_uuid)
            else:
                user=User(username=user,password=password)
            db.session.add(user)
            db.session.commit()
            print("恭喜註冊成功")
            return redirect(url_for('login'))
    
    return render_template('register.html',line_uuid=line_uuid)


@app.route('/line_notify',methods=['POST','GET'])
def line_notify():
    tokenState=User.query.filter(User.username==flask_session['user']).first().NotifyToken
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
    User.query.filter_by(username=flask_session['user']).update({'NotifyToken':user_token})
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
    user_token=User.query.filter(User.username==flask_session['user']).first().NotifyToken
    headers = {
        "Authorization": "Bearer "+user_token,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    # line端token綁api狀態
    msg = requests.get("https://notify-api.line.me/api/status", headers=headers)
    line_tokenState=str(msg.json()["message"])
    if line_tokenState=='ok':
        # 解除line端token api
        msg=requests.post("https://notify-api.line.me/api/revoke", headers=headers)
        User.query.filter_by(username=flask_session['user']).update({'NotifyToken':'None'})
        db.session.commit()
        print(msg.json()["message"])
        return redirect(url_for('line_notify'))
    else:
        User.query.filter_by(username=flask_session['user']).update({'NotifyToken':'None'})
        db.session.commit()
        return redirect(url_for('line_notify'))

@app.route('/testform',methods=['POST','GET'])
def testform():
    if request.method == 'POST':
        G1_mac=request.form['mac']
        ip=request.form['ip']
        User.query.filter_by(username=flask_session['user']).update({'G1_mac':G1_mac,'ip':ip})
        db.session.commit()
    return render_template('testform.html')


@app.route('/html5_qrcode',methods=['GET'])
def html5_qrcode():
    return render_template('html5_qrcode.html')


@app.route('/Device_management',methods=['GET'])
def Device_management():
    array=[]
    # j=User.query.join(Notify_status,User.Line_uuid==Notify_status.Line_uuid)
    result =db.session.query(User.username,Notify_status.Device_Mac,Notify_status.Device_status).filter(User.username==flask_session['user']).filter(User.Line_uuid==Notify_status.Line_uuid).all()
    # for row in db.session.execute(stmt):
    #     print(f"{row.User.username} {row.Address.Device_Mac}")
    for i in range (len(result)):
        Device_Mac=result[i][1]
        Device_status=result[i][2]
        data={'Device_Mac':Device_Mac,'Device_status':Device_status}
        array.append(data)
    print(array)

    return render_template('Device_management.html',tabledata=array)