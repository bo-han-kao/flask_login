from array import array
from genericpath import exists
from tkinter import N
from flask import Flask, flash,render_template,request,redirect,url_for,session as flask_session
from urllib.parse import parse_qs
import urllib.parse as urlparse
import base64
import time
import os
import crypt
import requests
from sqlalchemy import false, join, null, table,text, true, values,update,exists
from sqlalchemy.sql import select

from app import app,bcrypt,db
from GoogleRecaptcha import GoogleRecaptcha

from models import User,Notify_status
import json
# -------------------------------mqtt use-------------------------
import configparser
import json
import traceback
from collections import defaultdict
from package import mqtt_config, db_op
# -------------------------------mqtt use-------------------------
# Read configuration file.
config = configparser.ConfigParser()
config.read('config.ini')
MQTT_BROKER_HOST = config.get('DEFAULT', 'MQTT_BROKER_HOST')
MQTT_BROKER_PORT = config.getint('DEFAULT', 'MQTT_BROKER_PORT')
SERVER_HOST = config.get('DEFAULT', 'SERVER_HOST')
SERVER_PORT = config.getint('DEFAULT', 'SERVER_PORT')
SERVER_URL = f'http://{SERVER_HOST}:{SERVER_PORT}/v2'

DEVICE_TYPE = {
    0: 'PowerMeter',
    1: 'smart_watch',
    2: 'CO2_VOC_Temp',
    3: 'sensor',
    4: 'switch'
}

mqtt_dongle_data = defaultdict(lambda: defaultdict(dict))
# -------------------------------mqtt use-------------------------
@app.before_request
def login_require():
    if request.path in ['','/login','/register','/powermeter_list_device'] or '/static/' in request.path:
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
    key = "wentaiwentaiwentaiwentai"
 
    # print(crypt_key,decrypt_key)
    # print((crypt.decrypt(key,'M548aeQznqJti0TnCPKlZY%2FdNFIUB4anwaxDNMsjuNdOcPK2GWytEjk+NK3KD1OS51K4vlop403V+2XdPl6Uvw==')))
    # print(parsed)
    # testdecrypt=decrypt(key,parsed)
    # 看網址是否含LINE_UUID參數
    
    groupQuery = 'key' in parse_qs(parsed.query)
    if groupQuery == True:
        # print(parse_qs(parsed.query)['key'][0])
        crypt_key=parse_qs(parsed.query)['key'][0]
        decrypt_key = crypt.decrypt(key,crypt_key) 
        # 取得line_uuid
        line_uuid=decrypt_key.split('=')[1]
        line_uuid=line_uuid.split('&')[0]
        # print(line_uuid)
        db_line_uuid=User.query.filter_by(Line_uuid=line_uuid).first()
        if str(db_line_uuid)=='None':
            return redirect(url_for('register',key=crypt_key))
    if request.method == 'POST':
        font_end_data=request.json
        user=font_end_data['username']
        password=font_end_data['password']
        # recaptcha_token=font_end_data['recaptcha_token']
        print(user,password)
        # 找碴資料庫USER是否存在
        user=user.lower()
        user=User.query.filter_by(username=user).first()
        # 判斷帳號密碼是否輸入正確
        if user and bcrypt.check_password_hash(user.password,password):
            flask_session['user'] = user.username
            return  {"status":"200","msg":"success login","redirect":url_for('user')}        
        else:
            return {"status":"401","msg":"登入失敗"}
       
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
    key = "wentaiwentaiwentaiwentai"
    groupQuery = 'key' in parse_qs(parsed.query)
    
    if groupQuery==True:
        # print(parsed.query)
        try:
            ID_key=parsed.query.split('=')[1]
            ID_key=crypt.decrypt(key,ID_key)
            line_uuid = parse_qs(ID_key)['ID'][0]
            if request.method == 'POST':
                font_end_data=request.json
                user=font_end_data['username']
                password=font_end_data['password']
                # recaptcha_token=font_end_data['recaptcha_token']
                #  有重複user處理
                if User.query.filter_by(username=user.lower()).first():
                    return {"status":"401","msg":"duplicate_name"}
                
                elif User.query.filter_by(Line_uuid=line_uuid).first():
                    return {"status":"401","msg":"duplicate_Line_id"}

                else:
                    password=bcrypt.generate_password_hash(password).decode('utf-8')
                    user=User(username=user.lower(),password=password,Line_uuid=line_uuid)
                    # print(user)
                    db.session.add(user)
                    db.session.commit()
                    return {"status":"200","msg":"success register","redirect":url_for('login')}
        except:
            return('line帳戶有誤')
    else:
        return ('請從line_註冊帳戶')
    # if request.method == 'POST':
    #     user=request.form['user']
    #     password=request.form['password']
    
    #     # 有重複user處理
    #     if User.query.filter_by(username=user).first():
    #         if line_uuid:
    #             return render_template('register.html',register_state='名稱已被註冊',line_uuid=line_uuid)

    #     else:
    #         # 對密碼加密(hash)
    #         password=bcrypt.generate_password_hash(password).decode('utf-8')
    #         if line_uuid:
    #             line_uuid=request.form['Line_uuid']
    #             user=User(username=user,password=password,Line_uuid=line_uuid)
    #         else:
    #             user=User(username=user,password=password)
                
    #         db.session.add(user)
    #         db.session.commit()
    #         return redirect(url_for('login'))
    
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
        "redirect_uri": 'http://10.10.10.83:5000/line_notify_bind',
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
        # User.query.filter_by(username=flask_session['user']).update({'G1_mac':G1_mac})
        newDevice=Notify_status(username=flask_session['user'],Device_Mac=G1_mac,Device_type='occupancy',Device_status=1)
        db.session.add(newDevice)
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
    result =db.session.query(User.username,Notify_status.Device_Mac,Notify_status.Device_status,Notify_status.Device_type).filter(User.username==flask_session['user']).filter(User.username==Notify_status.username).all()
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
        user=User.query.filter_by(username=flask_session['user']).first().username
        font_end_data=request.json
        for i in font_end_data:
            Notify_status.query.filter(Notify_status.username==user , Notify_status.Device_Mac==i['devicename']).update({'Device_status':i['status']})
            db.session.commit()
        return {'state':'200'}


@app.route('/Device_management/delete',methods=['POST'])
def Device_management_delete():
   if request.method == 'POST':
        font_end_data=request.json
        user=User.query.filter_by(username=flask_session['user']).first().username
        Notify_status.query.filter_by(username=user,Device_Mac=font_end_data['delete_mac']).delete()
        # print(Notify_status.query.filter_by(username=user).first())
        db.session.commit()
        return {'state':'200','msg':'delete ok'}

@app.route('/Device_management/deleteall',methods=['POST'])
def Device_management_deleteall():
   if request.method == 'POST':
        user=User.query.filter_by(username=flask_session['user']).first().username
        Notify_status.query.filter_by(username=user).delete()
        db.session.commit()
        return {'state':'200','msg':'delete_all ok'}

# 用AJAX取得資料
# @app.route('/powermeter_list_device',methods=['GET'])
# def powermeter_list_device():
#     mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
#     if mqtt_dongle_id=='' or mqtt_dongle_id=='None' or mqtt_dongle_id==null:
#         return {'code':'200','msg':'no found dongle_id'}
#     else:
#         powermeter_device=[]
#         for key in mqtt_dongle_data[mqtt_dongle_id].keys():
#             if key:
#                 powermeter_device.append({'device':key,'deviceType':'PowerMeter'})       
#         return json.dumps(powermeter_device)

@app.route('/powermeter',methods=['GET','POST'])
def powermeter():
    if request.method == 'POST':
        mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
        parsed = urlparse.urlparse(request.url)
        meter_devicName=parsed.query.split('=')[1]
        if request.json['control']=='relay_control':
            relay_status= request.json['relay_status']
            PublishRelay(mqtt_dongle_id,meter_devicName,relay_status)
            print(relay_status)
            return({'relay_status':relay_status})
        else:
            to_fondend_data={
            'watt_hour':'',
            'watt':'',
            'volt':'',
            'current':'',
            'frequency':'',
            'rssi':'',
            'data_type':''
            }
            pmd = mqtt_dongle_data[mqtt_dongle_id][meter_devicName][1:]
            print(pmd)
            for key, val in zip(to_fondend_data, pmd):
                to_fondend_data[key] = val
            # print(to_fondend_data)
            return(json.dumps(to_fondend_data))
            
    return render_template('powermeter.html')

@app.route('/CO2',methods=['GET','POST'])
def CO2():
    if request.method=='POST':
        to_fondend_data={
                'battery':'',
                'LED':'',
                'TVOC':'',
                'humidity':'',
                'temperature':'',
                'co2':'',
                'rssi':'',
                'data_type':''
                }
        mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
        parsed = urlparse.urlparse(request.url)
        CO2_devicName=parsed.query.split('=')[1]
        pmd = mqtt_dongle_data[mqtt_dongle_id][CO2_devicName][1:]
        for key, val in zip(to_fondend_data, pmd):
                to_fondend_data[key] = val
        return(json.dumps(to_fondend_data))
    return render_template('CO2.html')

@app.route('/watch',methods=['GET','POST'])
def watch():
    if request.method=='POST':
        
        to_fondend_data={
                'Blood_Oxygen':'',
                'Respiration_rate':'',
                'Stress':'',
                'RRI(HRV)':'',
                'Stress_level':'',
                'SBP':'',
                'DBP':'',
                'Calories':'',
                'Temperature':'',
                'Steps':'',
                'Heart_rate':'',
                'SOS':'',
                'Battery':'',
                'RSSI':''
                }
        mqtt_dongle_id=User.query.filter(User.username==flask_session['user']).first().mqtt_dongle_id
        parsed = urlparse.urlparse(request.url)
        watch_devicName=parsed.query.split('=')[1]
        print(watch_devicName,mqtt_dongle_id)
        pmd = mqtt_dongle_data[mqtt_dongle_id][watch_devicName][1:]
        print(pmd)
        for key, val in zip(to_fondend_data, pmd):
                to_fondend_data[key] = val
        return(json.dumps(to_fondend_data))
    
    return render_template('watch.html')
# -------------------------------mqtt code-------------------------
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    # client.subscribe('command/#')
    client.subscribe('mqtt_dongle/read/+')
    # client.subscribe('get/notify/+')
    # client.subscribe('set/notify/#')
    # client.subscribe('MeetingRoomOccupancy')
    # client.subscribe('MeetingRoomOccupancyJPEG')
    client.subscribe('get/jpeg')

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        try:
            payload = json.loads(msg.payload)
        except Exception:
            payload = json.loads('{' + msg.payload.decode() + '}')
        # print(f'Topic: {topic}')
        # print(f'Payload: {payload}')
        if topic.startswith('command/group/'):
            control_light(payload, topic)
        elif topic.startswith('command/smart_plug/'):
            relay_on_off(payload, topic)
        elif topic.startswith('mqtt_dongle/read/'):
            get_device_data(topic, payload)
        elif topic.startswith('set/notify/'):
            set_device_notify(payload, topic)
        elif topic.startswith('get/notify/'):
            get_device_notify(client, payload, topic)
        elif topic == 'MeetingRoomOccupancyJPEG':
            push_occupancy_jpeg(payload)
        elif topic == 'MeetingRoomOccupancy':
            push_occupancy_message(payload)
        elif topic == 'get/jpeg':
            get_occupancy_jpeg(client, payload)
    except Exception:
        traceback.print_exc()

def get_occupancy_jpeg(client, payload):
    line_uuid = payload['line_uuid']
    db = db_op.Database()
    with db:
        g1_mac = db.get_g1_mac(line_uuid)
    with open(f'app/static/img/occupancy_{g1_mac}.jpeg', 'rb') as f:
        image = base64.b64encode(f.read()).decode()
    client.publish('get/jpeg/G1', image, qos=1)


def push_occupancy_message(payload):
    cameraid = payload['CameraID']
    db = db_op.Database()
    with db:
        tokens = db.get_tokens(cameraid, 'occupancy')
    for token in tokens:
        if payload['Occupancy']:
            message = "有人存在!!"  # 要發送的訊息
            image = "app/static/img/G1 In.png"
        else:
            message = "有人離開!!"  # 要發送的訊息
            image = "app/static/img/G1 out.png"
        post_data(token[0], message, image)


def push_occupancy_jpeg(payload):
    cameraid = payload['CameraID']
    filename = f'app/static/img/occupancy_raw_{cameraid}.jpeg'
    jpegpayload = payload['JPEGPayload']
    with open(filename, 'a') as f:
        f.write(jpegpayload)
    if payload['TotalMsg'] == payload['CurrentIdx']:
        with open(filename, 'r') as raw:
            with open(f'app/static/img/occupancy_{cameraid}.jpeg', 'wb') as ocu:
                ocu.write(base64.b64decode(raw.read()))
        os.remove(filename)
        db = db_op.Database()
        with db:
            tokens = db.get_tokens(cameraid, 'occupancy')
        for token in tokens:
            message = '圖片推播'
            image = f'app/static/img/occupancy_{cameraid}.jpeg'
            post_data(token[0], message, image)


def get_device_notify(client, payload, topic):
    line_uuid = payload['line_uuid']
    type_ = topic.split('/')[-1]
    db = db_op.Database()
    with db:
        notify = db.get_notify(line_uuid, type_)
    publish_payload = {
        'line_uuid': line_uuid,
        'type': type_,
        'notify': bool(notify[0])
    }
    client.publish(f'get/notify/{type_}/return', json.dumps(publish_payload), qos=1)


def set_device_notify(payload, topic):
    line_uuid = payload['line_uuid']
    type_ = topic.split('/')[-1]
    db = db_op.Database()
    with db:
        db.set_notify(line_uuid, type_, payload['notify'])


def get_device_data(topic, payload):
    mqtt_dongle_id = topic.split('/')[-1]
    data = payload['device']['data']
    device_type = DEVICE_TYPE[data[-1]]
    device_id = data[0]
    if device_type in ('sensor', 'switch'):
        on_off = data[1][-4:-2]
        # print(on_off)
        db = db_op.Database()
        with db:
            tokens = db.get_tokens(device_id, device_type, mqtt_dongle_id)
        # print(tokens)
        if device_type == 'sensor' and on_off == '01':
            message = "有人闖入!!"  # 要發送的訊息
            image = "app/static/img/sensor.png"
            for token in tokens:
                post_data(token[0], message, image)
        elif device_type == 'switch' and on_off == '00':
            message = '有人開窗!!'
            image = 'app/static/img/switch.png'
            for token in tokens:
                post_data(token[0], message, image)
    elif device_type in ('PowerMeter', 'CO2_VOC_Temp','smart_watch'):
        mqtt_dongle_data[mqtt_dongle_id][device_id] = data
    db = db_op.Database()
    with db:
        db.save_device_data(device_id, mqtt_dongle_id, device_type)


def relay_on_off(payload, topic):
    json_ = {
        'cmd': 'write',
        'device_id': payload['device_id'],
        'func': 'RELAY',
        'data': '',
        'dongle_ip': payload['dongle_ip']
    }
    if topic.endswith('/relay_on'):
        json_['data'] = 'ON'
    elif topic.endswith('/relay_off'):
        json_['data'] = 'OFF'
    resp = requests.post(f'{SERVER_URL}/beacon/smartplug/relay', json=json_)
    print(f'Response Content: {resp.content.decode("utf-8")}')


def control_light(payload, topic):
    json_ = {
        'group': {
            'id': payload['id'],
            'uniAddress': payload['uniAddress'],
            'state': {}
        }
    }
    if topic.endswith('/all_on'):
        json_['group']['state']['onOff'] = 1
    elif topic.endswith('/all_off'):
        json_['group']['state']['onOff'] = 0
    elif topic.endswith('/all_yellow'):
        json_['group']['state']['cct'] = 0
    elif topic.endswith('/all_white'):
        json_['group']['state']['cct'] = 255
    elif topic.endswith('/all_cct_mid'):
        json_['group']['state']['cct'] = 128
    elif topic.endswith('/all_level_max'):
        json_['group']['state']['level'] = 255
    elif topic.endswith('/all_level_min'):
        json_['group']['state']['level'] = 1
    elif topic.endswith('/all_level_mid'):
        json_['group']['state']['level'] = 128
    resp = requests.patch(f'{SERVER_URL}/group', json=json_)
    print(f'Response Content: {resp.content.decode("utf-8")}')


def subscribe():
    client = mqtt_config.MQTTConfig()
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)
        else:
            break
    print('Start subscribing...')
    client.loop_start()
    return client


def post_data(token, message, image):
    try:
        if token is not None:
            url = "https://notify-api.line.me/api/notify"
            headers = {
                'Authorization': f'Bearer {token}'
            }
            payload = {
                'message': message
            }
            files = {
                'imageFile': open(image, 'rb')
            }
            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                files=files
            )
            if response.status_code == 200:
                print(f"Success -> {response.text}")
            else:
                print(response.content)
    except Exception as _:
        print(_)


client = subscribe()

def PublishRelay(mqtt_id,device_Mac,relay_status):
    payload=f'{{"{{"action":"set_relay","device_id":"{device_Mac}","relay":"{relay_status}"}}"}}'
    client.publish("mqtt_dongle/write/"+mqtt_id, payload)
    print("mqtt_dongle/write/"+mqtt_id)
    print(payload)
    print("startpub")
    
# PublishRelay("F08E4B12E4CE","C5B024672C48","OFF")



# -------------------------------mqtt code-------------------------