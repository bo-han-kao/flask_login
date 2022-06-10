from collections import UserList
import email
from msilib.schema import Class
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from models import User
from flask import flash

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=6,max=20)],render_kw={"class":"alert alert-error"})
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)],render_kw={"class":"alert alert-error"})
    # email=StringField('email',validators=[DataRequired(),Email()])
    # confirm=PasswordField('confirm_Password',validators=[DataRequired(),EqualTo('password')])
    # recaptcha = RecaptchaField()
    submit=SubmitField('Register')
    # 改顯示判斷
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already')