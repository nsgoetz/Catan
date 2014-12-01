from app import db
from sqlalchemy_utils import PasswordType

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=False, unique=False)
  email = db.Column(db.String(120), index=True, unique=True)
  #passhash = db.Column(db.PasswordType(schemes='CRYPT', index=False, unique=False)
  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return '<User id:%r name:%r email:%r>' % (self.id, self.name, self.email)

class Player(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  color = db.Column(db.Integer, nullable=False) #rrrgggbbb

  brick = db.Column(db.Integer, default=0, nullable=False)
  ore = db.Column(db.Integer, default=0, nullable=False)
  lumber = db.Column(db.Integer, default=0, nullable=False)
  wool = db.Column(db.Integer, default=0, nullable=False)
  grain = db.Column(db.Integer, default=0, nullable=False)
  devcards = db.Column(db.Text)

  cities = db.Column(db.Text)
  settlements = db.Column(db.Text)
  roads = db.Column(db.Text)

  largest_army = db.Column(db.Bool, default=False)
  knights_played = db.Column(db.Integer, default=0, nullable=False)

  longest_road = db.Column(db.Bool, default=False, nullable=False)
  longest_road_len = db.Column(db.Integer, default=0, nullable=False)


  def __repr__(self):
    return '<Player id:%r>' % (self.id)

class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  players = db.relationship('Player', backref='game', lazy='dynamic') #?how
  current_player = db.Column(db.Integer, db.ForeignKey('player.id'))
  settup_round = db.Column(db.Boolean)
  started = db.Column(db.Boolean, default = False)

  buildings = db.Column(db.Text) #(row,col) -> (owner, level) (defualt None)
  roads = db.Column(db.Text)
  hexes = db.Column(db.Text) #(hex_row, hex_col) -> (resource, probability)
  probabilities = db.Column(db.Text)
  robber_location = db.Column(db.Integer)

  largest_army_player = db.Column(db.Integer, db.ForeignKey('player.id'))
  largest_army_size = db.Column(db.Integer, default=2)
  longest_road_player = db.Column(db.Integer, db.ForeignKey('player.id'))
  longest_road_size = db.Column(db.Integer, default=4)
  #passhash = db.Column(db.PasswordType(schemes='CRYPT', index=False, unique=False)

  def __repr__(self):
    return '<Game %r>' % (self.nickname)
