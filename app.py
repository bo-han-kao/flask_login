from ensurepip import bootstrap
from turtle import title
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

app=Flask(__name__)
bootstrap=Bootstrap(app)
db=SQLAlchemy(app)

app.config.from_object(config)

@app.route('/')
def index():
    title='web app'
    fakedata=[
        'data1',
        'data2',
        'data3'
    ]
    return render_template('index.html',title=title,data=fakedata)

if __name__=='__main__':
    app.run(debug=True)