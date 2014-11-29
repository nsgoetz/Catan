from flask import Flask, session, redirect, url_for, escape, \
      request, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, PasswordField, validators
from wtforms.validators import *

class SignupForm(Form):
    username = TextField('Email', validators=[
                                    InputRequired(),
                                    Email(message='Must be a valid email adress')])
    password = PasswordField('Password', validators=[
                                    InputRequired(),
                                    Length(min=8)])
    confirm  = PasswordField('Confirm Password', validators=[
                                    InputRequired(),
                                    EqualTo('password', message='Passwords must match')])

    submit_button = SubmitField('Submit Form')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


def create_app(configfile=None):
  app = Flask(__name__)
  Bootstrap(app)
  AppConfig(app, configfile)
  # in a real app, these should be configured through Flask-Appconfig?
  app.config['SECRET_KEY'] = '\xe9\xc8\x1b\x8f\x1c\xaa\x82X\xb0\xb8\xa0`\xbc\x98z\x82\xe1#~9\xda\x85a\xf9'

  @app.route('/')
  def index():
    if 'username' in session:
      status = 'Logged in as %s' % escape(session['username'])
    else:
      status = 'You are not logged in'
    return render_template("index.html", status=status)

  return app

app = create_app()
@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'GET':
    form = SignupForm()
    form.validate_on_submit() #to get error messages to the browser
    return render_template("sign_up.html", form=form)
  else:
    return create_account()

def create_account():
  form = SignupForm(username=request.args.get('username'),
                    password=request.args.get('password'),
                    confirm=request.args.get('confirm'))
  if form.validate():
    session['username'] = request.form['username']
    return redirect(url_for('index'))
  else:
    print "here"
    return render_template("sign_up.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)