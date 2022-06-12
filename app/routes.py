from flask import Flask, flash,render_template,request,redirect,url_for,session
from urllib.parse import parse_qs
import urllib.parse as urlparse
from app import app,bcrypt,db

# from forms import RegisterForm
from models import User


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
    # form=RegisterForm()
   
    # flash('registeration success',category='success')


    
    # if form.validate_on_submit():
    #     username=form.username.data
    #     password=bcrypt.generate_password_hash(form.password.data)
    #     print(username,password)
    #     user=User(username=username,password=password)
    #     db.session.add(user)
    #     db.session.commit()
    parsed = urlparse.urlparse(request.url)
    groupQuery = 'username' in parse_qs(parsed.query)
    front_end_data={'UserNameText':''}
    if groupQuery:
        front_end_data['UserNameText']=parse_qs(parsed.query)['username'][0]

    if request.method == "POST":
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
   
    return render_template('register.html',UserNameText=front_end_data['UserNameText'])