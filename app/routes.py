from flask import Flask, flash,render_template,request
from urllib.parse import parse_qs
import urllib.parse as urlparse
from app import app,bcrypt,db

from forms import RegisterForm
from models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    parsed = urlparse.urlparse(request.url)
    groupQuery = 'username' in parse_qs(parsed.query)

    flash('registeration success',category='success')
    
    if groupQuery:
        form.username.data=parse_qs(parsed.query)['username'][0]
    if form.validate_on_submit():
        username=form.username.data
        password=bcrypt.generate_password_hash(form.password.data)
        print(username,password)
        user=User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
       
    return render_template('register.html',form=form)