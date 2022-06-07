from ensurepip import bootstrap
from turtle import title
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
app=Flask(__name__)
bootstrap=Bootstrap(app)
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