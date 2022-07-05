from array import array
from genericpath import exists
from tkinter import N
from flask import Flask, flash,render_template,request,redirect,url_for,session as flask_session
from urllib.parse import parse_qs
import urllib.parse as urlparse

from sqlalchemy import false, join, null, table,text, true, values,update,exists
from sqlalchemy.sql import select

from app import app,bcrypt,db
import requests
# from forms import RegisterForm
from models import User,Notify_status
import json
# -------------------------------mqtt use-------------------------
import configparser
import json
import traceback
from collections import defaultdict
from package import mqtt_config

# Read configuration file.
config = configparser.ConfigParser()
config.read('config.ini')
MQTT_BROKER_HOST = config.get('DEFAULT', 'MQTT_BROKER_HOST')
MQTT_BROKER_PORT = config.getint('DEFAULT', 'MQTT_BROKER_PORT')

DEVICE_TYPE = {
    0: 'power_meter',
    1: 'smart_watch',
    2: 'sensor',
    3: 'switch'
}

power_meter_data = defaultdict(lambda: defaultdict(dict))
# -------------------------------mqtt use-------------------------

@app.before_request
def login_require():
    if request.path in ['','/','/login','/register','/powermeter_list_device'] or '/static/' in request.path:
        return None
    flask_session.permanent = True
    user=flask_session.get('user') 
    # print(user)
    if user==None:
        return redirect('/login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    # 網址資訊
    parsed = urlparse.urlparse(request.url)
    # 看網址是否含LINE_UUID參數
    groupQuery = 'LINE_UUID' in parse_qs(parsed.query)
    # print(groupQuery)
    if groupQuery == True:
        # 取得line_uuid
        line_uuid=parsed.query.split('=')[1]
        db_line_uuid=User.query.filter_by(Line_uuid=line_uuid).first()
        if str(db_line_uuid)=='None':
            return redirect(url_for('register',LINE_UUID=line_uuid))

    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']
        # 找碴資料庫USER是否存在
        user=User.query.filter_by(username=user).first()
        # 判斷帳號密碼是否輸入正確
        if user and bcrypt.check_password_hash(user.password,password):
            flask_session['user'] = user.username
            return redirect(url_for('user'))
        else:
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
    if groupQuery==True:
        line_uuid=parsed.query.split('=')[1]
    
    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']
    
        # 有重複user處理
        if User.query.filter_by(username=user).first():
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
            return redirect(url_for('login'))
    
    return render_template('register.html',line_uuid=line_uuid)


@app.route('/line_notify',methods=['POST','GET'])
def line_notify():
    tokenState=User.query.filter(User.username==flask_session['user']).first().NotifyToken
    # print(tokenState)
   
    return render_template('line_notify.html',tokenState=str(tokenState))


@app.route('/line_notify_bind',methods=['POST','GET'])
def line_notify_bind():
    notify_code=request.args.get('code')
    # print(notify_code)
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
    # print('使用者token:'+user_token)
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
        return redirect(url_for('line_notify'))
    else:
        User.query.filter_by(username=flask_session['user']).update({'NotifyToken':'None'})
        db.session.commit()
        return redirect(url_for('line_notify'))

@app.route('/testform',methods=['POST','GET'])
def testform():
    if request.method == 'POST':
        G1_mac=request.form['mac']
        User.query.filter_by(username=flask_session['user']).update({'G1_mac':G1_mac})
        db.session.commit()
    return render_template('testform.html')


@app.route('/html5_qrcode',methods=['GET'])
def html5_qrcode():
    return render_template('html5_qrcode.html')

@app.route('/html5_qrcode/edit',methods=['POST'])
def html5_qrcode_edit():
   if request.method == 'POST':
        font_end_data=request.json
        User.query.filter(User.username==flask_session['user']).update({'mqtt_dongle_id':font_end_data['mqtt_id']})
        db.session.commit()
        return {'state':'200'}

@app.route('/Device_management',methods=['GET'])
def Device_management():
    array=[]
    # j=User.query.join(Notify_status,User.Line_uuid==Notify_status.Line_uuid)
    result =db.session.query(User.username,Notify_status.Device_Mac,Notify_status.Device_status,Notify_status.Device_type).filter(User.username==flask_session['user']).filter(User.Line_uuid==Notify_status.Line_uuid).all()
    # for row in db.session.execute(stmt):
    #     print(f"{row.User.username} {row.Address.Device_Mac}")
    for i in range (len(result)):
        Device_Mac=result[i][1]
        Device_status=result[i][2]
        Device_type=result[i][3]
        data={'Device_Mac':Device_Mac,'Device_status':Device_status,'Device_type':Device_type}
        array.append(data)
   

    return render_template('Device_management.html',tabledata=array)


@app.route('/Device_management/edit',methods=['POST'])
def Device_management_edit():
   if request.method == 'POST':
        # p=db.session.query(Notify_status).filter(User.username==flask_session['user'], User.Line_uuid==Notify_status.Line_uuid, Notify_status.Device_Mac=='EA083F58FDC4').update({Notify_status.Device_status: False}, synchronize_session='fetch')
        # p=db.session.query(Notify_status).filter_by( User.username=flask_session['user'] and User.Line_uuid=Notify_status.Line_uuid and  Notify_status.Device_Mac='EA083F58FDC4').update({Notify_status.Device_status: False}, synchronize_session='fetch')
        # stmt=(update(Notify_status).values(Device_status=0).where(Notify_status.Device_Mac=='EA083F58FDC4'))
        # p=update(Notify_status).values(Device_status=0).filter(exists().where(User.Line_uuid==Notify_status.Line_uuid , User.username=='jack' ,Notify_status.Device_Mac=='EA083F58FDC4'))
        user_lineuuid=User.query.filter_by(username=flask_session['user']).first().Line_uuid
        font_end_data=request.json
        for i in font_end_data:
            Notify_status.query.filter(Notify_status.Line_uuid==user_lineuuid , Notify_status.Device_Mac==i['devicename']).update({'Device_status':i['status']})
            db.session.commit()
        return {'state':'200'}

@app.route('/powermeter_list_device',methods=['GET'])
def powermeter_list_device():
    mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
    if mqtt_dongle_id=='' or mqtt_dongle_id=='None' or mqtt_dongle_id==null:
       
        return {'code':'200','msg':'no found dongle_id'}
    else:
        powermeter_device=[]
        for key in power_meter_data[mqtt_dongle_id].keys():
            if key:
                powermeter_device.append({'device':key,'deviceType':'PowerMeter'})
       
        return json.dumps(powermeter_device)




@app.route('/powermeter',methods=['GET','POST'])
def powermeter():
    if request.method == 'POST':
        to_fondend_data={
        'watt_hour':'',
        'watt':'',
        'volt':'',
        'current':'',
        'frequency':'',
        'rssi':'',
        'data_type':''
        }
        mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
        parsed = urlparse.urlparse(request.url)
        meter_devicName=parsed.query.split('=')[1]
        # print(power_meter_data[mqtt_dongle_id][meter_devicName])
        pmd = power_meter_data[mqtt_dongle_id][meter_devicName][1:]
        for key, val in zip(to_fondend_data, pmd):
            to_fondend_data[key] = val
        # print(to_fondend_data)
        return(json.dumps(to_fondend_data))
    return render_template('powermeter.html')




# -------------------------------mqtt code-------------------------
def on_connect(client, userdata, flags, rc):
    # print(f'Connected with result code {rc}')
    client.subscribe('mqtt_dongle/read/+')


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        try:
            payload = json.loads(msg.payload)
        except Exception:
            payload = json.loads('{' + msg.payload.decode() + '}')
        # print(f'Topic: {topic}')
        # print(f'Payload: {payload}')
        get_device_data(topic, payload)
    except Exception:
        traceback.print_exc()


def get_device_data(topic, payload):
    mqtt_dongle_id = topic.split('/')[-1]
    data = payload['device']['data']
    device_type = DEVICE_TYPE[data[-1]]
    device_id = data[0]
    if device_type == 'power_meter':
        
        power_meter_data[mqtt_dongle_id][device_id] = data
        # print(power_meter_data)

def subscribe():
    client = mqtt_config.MQTTConfig()
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        except Exception:
            traceback.print_exc()
        else:
            break
    print('Start subscribing...')
    client.loop_start()
    return client


client = subscribe()
# -------------------------------mqtt code-------------------------