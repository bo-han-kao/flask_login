import email
from msilib.schema import Class
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    # email=StringField('email',validators=[DataRequired(),Email()])
    confirm=PasswordField('confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')