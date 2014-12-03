import random
from app import models, db

VERTEX_ROWS = 12
VERTEX_COLS = 11
HEX_ROWS = 8
HEX_COLS = 5
POSSIBLE_COLORS = ["CornflowerBlue",
                   "Coral",
                   "DarkSalmon",
                   "LightGreen",
                   "RoyalBlue",
                   "Violet",
                   "FireBrick",
                   "OliveDrab",
                   "Aqua",
                   "White"]

def make_game(): #rgb
  buildings = make_possible_buildings()
  (hexes, probabilities, robber_location) = make_hexes(buildings)
  roads = make_possible_roads(buildings)
  game = models.Game(settup_round = True, started=False,
                     buildings = buildings, hexes = hexes,
                     probabilities = probabilities, roads = roads,
                     robber_location= robber_location,
                     colors_left=POSSIBLE_COLORS)
  db.session.add(game)
  db.session.commit()
  return game.id

def make_possible_buildings():
  buildings = {}
  rows, cols = VERTEX_ROWS, VERTEX_COLS
  for row in xrange(rows):
    for col in xrange(cols):
      #only add a 0 where there is a vertex (not in the middle of)
      if (((col%2 == 1) and (row%4 == 0 or row%4 == 3) or
        (col%2 == 0 and (row%4 == 1 or row%4 == 2))) and
        #hardcode removing corners
        #all verticies in the core exist
        ((col >= 2 and col <= cols - 3) or
        #inside cols
        ((abs((cols-1)/2-col) == 4) and
        row > (rows/2) - 4 and row < (rows/2)+4) or
        #outside cols
        ((abs((cols-1)/2-col) == 5) and
        (row > (rows/2) -2 and row < (rows/2) + 2)))):
          #finally add vertex
          buildings[(col, row)] = (None, 0)
  return buildings

def make_hexes(buildings):
  resources = (["brick",  "ore"] * 3) + (["lumber", "wool", "grain"] * 4) + ["desert"]
  p_distribution = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
  probabilities = {}
  hexes = {}
  for p in xrange(2,13):
    probabilities[p] = []
  for (col, row) in buildings:
    if ((row % 2 == 1) and ((col-1, row-1) in buildings) and
        ((col+1, row-1) in buildings) and (col, row-3) in buildings):
      if (len(resources) == 0):
        raise InsufficientResources
      else:
        rand_resource_index = random.randint(0, len(resources)-1)
        resource = resources.pop(rand_resource_index)
        if (resource == "desert"):
          hexes[(col, row)] = (resource, None)
          robber_location = (col, row)
        else:
          if (len(p_distribution) == 0):
            raise InsufficientProbabilities
          else:
            rand_p_index = random.randint(0, len(p_distribution)-1)
            probability = p_distribution.pop(rand_p_index)
            hexes[(col, row)] = (resource, probability)
            probabilities[probability].append((col, row))
  #if adjacent red probabilities = start over
  if ((len(resources) != 0) or (len(p_distribution) != 0)):
      raise InsufficientHexes
  return (hexes, probabilities, robber_location)

def make_possible_roads(buildings):
  roads = {} #((row1, col1), (row2, col2)) -> owner (defualt None, (row1 < row2))
  dirs = [(0, 1), (1, 1), (1, -1)]
  for (c, r) in buildings:
    for (dc, dr) in dirs:
      c2, r2 = c+dc, r+dr
      if (c2, r2) in buildings:
        roads[((c, r), (c2, r2))] = None
  return roads

def add_player(game_id, user_id, color):
  game = models.Game.query.get(game_id)
  if (len(game.players) < 4):
    p = models.Player(user_id = user_id, color=color, game_id=game_id)
    game.colors_left = filter(lambda x: x != color, game.colors_left)
    db.session.add(p)
    db.session.add(game)
    db.session.commit()
  print "added"
  return p.id

def remove_player(game_id, player_id):
  game = models.Game.query.get(game_id)
  game.players = filter(lambda x: x.id != player_id, game.players)
  db.session.add(game)
  db.session.commit

def start_game(game_id):
  game = models.Game.query.get(game_id)
  if (len(game.players) < 2):
    return (False, "Not Enough Players")
  else:
    #randomize player order
    players = game.players
    random.shuffle(players)
    for i in xrange(len(players)):
      p = players[i]
      p.order = i
      db.session.add(p)
    db.session.commit()
    game.current_player_id = filter(lambda x: x.order == 0, game.players)[0].id
    game.started = True
    db.session.add(game)
    db.session.commit()
    return (True, game_id)

def end_round_number(self):
  pass
