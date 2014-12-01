from flask import Flask, session, redirect, url_for, escape, \
      request, render_template, flash
from app import app, models, db
from forms import *
from GameController import *
from PlayerController import *
from BoardController import *

@app.route('/')
@app.route('/index')
def index():
  if 'email' in session and 'name' in session:
    status = 'Logged in as %s (%s)' % (escape(session['name']), escape(session['email']))
  else:
    status = 'You are not logged in'
  return render_template("index.html", status=status)

####USER MANAGEMENT

@app.route('/sign_up', methods=['POST','GET'])
def sign_up():
  if request.method == 'GET':
    form = SignupForm() if request.form == None else SignupForm(request.form)
    form.validate_on_submit() #to get error messages to the browser
    return render_template("sign_up.html", form=form)
  else:
    return create_account()

@app.route('/create_account', methods=['POST'])
def create_account():
  form = SignupForm(email=request.form.get('email'),
                    name=request.form.get('name'))
                    # password=request.args.get('password'),
                    # confirm=request.args.get('confirm'))
  email = request.form.get('email')
  name = request.form.get('name')
  if form.validate():
    if (models.User.query.filter_by(email=email).count() > 0):
      flash("That email already has an account")
      return redirect(url_for('sign_up'))
    session['email'] = email
    session['name'] = name
    u = models.User(email=email, name=name)
    db.session.add(u)
    db.session.commit()
    print "committed"
    return redirect(url_for('index'))
  else:
    print "here"
    return redirect(url_for('sign_up'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and (request.form.get('email') != None):
      email = request.form.get('email')
      if (models.User.query.filter_by(email=email).count() == 0):
        flash("We don't seem to have an account with that email")
      else:
        u = models.User.query.filter_by(email=email).first()
        session['email'] = u.email
        session['name'] = u.name
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('index'))


### GAME MANAGEMENT
@app.route('/board', methods=['GET'])
def board():
  return render_template("board.html")

@app.route('/create_game', methods=['GET'])
def create_game():
  data = request.data
  user_id = data['user_id']
  color = data['color']
  game_id = make_game(user_id, color)
  return redirect(url_for(get_game)+str(game_id))

@app.route('/game/<game_id>/', methods=['GET'])
def get_game(game_id):
  user_id = request.data[user_id]
  game = models.Game.query(id = game_id).first()
  if (user_id in game.players):
    #started
    return
  else:


