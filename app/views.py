from flask import Flask, session, redirect, url_for, escape, \
      request, render_template, flash
from app import app
from forms import *

@app.route('/')
@app.route('/index')
def index():
  if 'username' in session:
    status = 'Logged in as %s' % escape(session['username'])
  else:
    status = 'You are not logged in'
  return render_template("index.html", status=status)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'GET':
    form = SignupForm()
    form.validate_on_submit() #to get error messages to the browser
    return render_template("sign_up.html", form=form)
  else:
    return create_account()

def create_account():
  form = SignupForm(email=request.args.get('email'),
                    name=request.args.get('name'),
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

