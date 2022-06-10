import email
from ensurepip import bootstrap
from tkinter.tix import Form
from turtle import title
from wsgiref import validate
from flask import Flask, flash,render_template,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import parse_qs
import urllib.parse as urlparse
from flask_bcrypt import Bcrypt

from config import config
from forms import RegisterForm
from models import User


app=Flask(__name__)
app.config.from_object(config)
bootstrap=Bootstrap(app)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    parsed = urlparse.urlparse(request.url)
    groupQuery = 'username' in parse_qs(parsed.query)
    # print(groupQuery)
    # print(parse_qs(parsed.query)['username'][0])
    if groupQuery:
        form.username.data=parse_qs(parsed.query)['username'][0]
    if form.validate_on_submit():
        username=form.username.data
        password=bcrypt.generate_password_hash(form.password.data)
        print(username,password)
        # user=User(username=username,password=password)
        # db.session.add(user)
        # db.session.commit()
        # flash('registeration success',category='sucrss')
    return render_template('register.html',form=form)

if __name__=='__main__':
    app.run(debug=True)