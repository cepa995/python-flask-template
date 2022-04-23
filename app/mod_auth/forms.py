# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import Form, StringField, PasswordField # BooleanField
# Import Form validators
from wtforms.validators import DataRequired,  EqualTo


# Define the login form (WTForms)

class LoginForm(Form):
    username    = StringField('username', [
                DataRequired(message='Forgot your username?')])
    password    = PasswordField('password', [
                DataRequired(message='Must provide a password.')])

class RegisterForm(Form):
    username    = StringField('username', [
                DataRequired(message='Forgot your username?')])
    password    = PasswordField('password', [
                DataRequired(message='Must provide a password.')])
