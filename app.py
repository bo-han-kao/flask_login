from turtle import title
from flask import Flask,render_template
app=Flask(__name__)

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