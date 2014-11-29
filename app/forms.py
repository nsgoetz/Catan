from flask_wtf import Form, RecaptchaField
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, PasswordField, validators
from wtforms.validators import *

class SignupForm(Form):
  email = TextField('Email', validators=[
                              InputRequired(),
                              Email(message='Must be a valid email adress')])
  name = TextField('Name/Nickname', validators=[InputRequired(), Length(min=2)])
  password = PasswordField('Password', validators=[
                                  InputRequired(),
                                  Length(min=8)])
  confirm  = PasswordField('Confirm Password', validators=[
                                  InputRequired(),
                                  EqualTo('password', message='Passwords must match')])

  submit_button = SubmitField('Submit Form')

  def validate_hidden_field(form, field):
    raise ValidationError('Always wrong')
