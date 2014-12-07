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
  user = db.relationship('User', backref='players')#, foreign_keys="user.id")
  game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
  game = db.relationship('Game', backref='players', foreign_keys="Player.game_id")
  color = db.Column(db.String(80)) #rrrgggbbb
  order = db.Column(db.Integer)

  resources = db.Column(db.PickleType)
  devcards = db.Column(db.PickleType)

  cities = db.Column(db.PickleType)
  settlements = db.Column(db.PickleType)
  roads = db.Column(db.PickleType)

  largest_army = db.Column(db.Boolean, default=False)
  knights_played = db.Column(db.Integer, default=0, nullable=False)

  longest_road = db.Column(db.Boolean, default=False, nullable=False)
  longest_road_len = db.Column(db.Integer, default=0, nullable=False)


  def __repr__(self):
    return '<Player id:%r user_id:%r game_id:%r>' % (self.id, self.user_id, self.game_id)

class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  current_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
  current_player = db.relationship('Player', backref='players', foreign_keys='Game.current_player_id')
  settup_round = db.Column(db.Boolean)
  started = db.Column(db.Boolean, default = False)
  colors_left = db.Column(db.PickleType)

  buildings = db.Column(db.PickleType) #(row,col) -> (owner, level) (defualt None)
  roads = db.Column(db.PickleType)
  hexes = db.Column(db.PickleType) #(hex_row, hex_col) -> (resource, probability)
  probabilities = db.Column(db.PickleType)
  robber_location = db.Column(db.PickleType)

  largest_army_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
  largest_army_player = db.relationship('Player', foreign_keys='Game.largest_army_player_id')
  longest_road_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
  longest_road_player = db.relationship('Player', foreign_keys='Game.longest_road_player_id')
  #passhash = db.Column(db.PasswordType(schemes='CRYPT', index=False, unique=False)

  def __repr__(self):
    return '<Game %r>' % (self.id)
