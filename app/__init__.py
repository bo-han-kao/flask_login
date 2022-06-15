from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import config

app=Flask(__name__)
app.config.from_object(config)
bootstrap=Bootstrap(app)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)


from app.routes import *

