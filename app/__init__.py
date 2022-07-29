from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import config
from flask_recaptcha import ReCaptcha

app=Flask(__name__)
app.config.from_object(config)
bootstrap=Bootstrap(app)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
recaptcha = ReCaptcha(app)

from app.routes import *

