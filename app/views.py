from flask import Flask, session, redirect, url_for, escape, \
      request, render_template, flash, jsonify, json, Response
from app import app, models, db
from forms import *
from GameController import *
from PlayerController import *
from BoardController import *

@app.route('/')
@app.route('/index')
def index():
  if 'user_id' in session:
    u = models.User.query.get(session["user_id"])
    print session["user_id"]
    status = 'Logged in as %s (%s)' % (escape(u.name), escape(u.email))
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
    u = models.User(email=email, name=name)
    db.session.add(u)
    db.session.commit()
    print "committed"
    session["user_id"] = u.id
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
        session["user_id"] = u.id
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
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

@app.route('/<game_id>', methods=['GET'])
def get_game(game_id):
  if (request.args.get("atr") != None):
    return game_state(game_id, request.args.get("atr"))
  user = models.User.query.get(session["user_id"])
  game = models.Game.query.get(int(game_id))
  if (user in map(lambda x: x.user, game.players)):
    if (game.started):
      return board()
    else:
      #notstarted
      return "waiting for game to start"
  else:
    if (game.started):
      flash("That game has already started. You can only see games you are in.")
      return redirect(url_for("index"))
    else:
      return "you must request to join that game"

def game_state(game_id, atr):
  user = models.User.query.get(session["user_id"])
  game = models.Game.query.get(int(game_id))
  player_list = filter(lambda x: x.user == user, game.players)
  if (len(player_list) == 0):
    return (False, "You are not playing the game")
  else:
    d = game.__dict__
    del d['_sa_instance_state']
    d['players'] = map(lambda x: x.id, d['players'])
    return jsonify(**d)


# @app.route('/game/<game_id>', methods=['POST'])
def player_state(game_id):
  user = models.User.query.get(session["user_id"])
  game = models.Game.query.get(int(game_id))
  player_list = filter(lambda x: x.user == user, game.players)
  if (len(player_list) == 0):
    return (False, "You are not playing the game")
  else:
    player = player_list[0]
    dat = flask.jsonify(**(player.__dict__))
    return Response(dat, status=200, mimetype="application/json")


