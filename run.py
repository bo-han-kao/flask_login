from app import app,db
from flask_cors import CORS
if __name__=='__main__':
    cors=CORS(app,resources=r'/*')
    db.create_all()
    app.run(debug=True,host='0.0.0.0',port=5000)