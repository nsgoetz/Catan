import random
from app import models, db

class Board(object):

  def __init__(self):
    #self.robber_location =
    #edges don't exist until we build them? or not.
    #build board
    #define a hex by the top vertex
    self.id = None
    self.vertex_rows = 12
    self.vertex_cols = 11
    self.hex_rows = 8
    self.hex_cols = 5
    self.buildings = {} #(row,col) -> (owner, level) (defualt None)
    self.roads = {}
    self.hexes = {} #(hex_row, hex_col) -> (resource, probability)
    self.probabilities = {}
    self.make_possible_buildings()
    self.make_hexes()
    self.make_possible_roads()
    self.round_number = -2 #over stepping bounds?
    self.building_costs = {"dev_card": {"ore":1, "wool":1, "grain":1},
                           "settlement": {"brick":1, "lumber":1, "wool":1, "grain":1},
                           "city": {"ore":3,"grain":2},
                           "road": {"wood":1, "brick":1}}
    self.players = [] #players
    self.current_player = None #self.players[0]
    self.largest_army_player = None
    self.longest_road_player = None
    self.longest_road_len = 4
    self.settup_round = True
    #resouces left?


  def build_initial_settlement(self, player, vertex):
    #add more validity checks
    if (self.buildings[vertex] != None):
      return False
    else:
      self.buildings[vertex] = player
      player.settlements.add(vertex)
      if (self.round_number == -1): #first round_number is -2, second is -1 - they're special
        #give resouces
        #vertext can always be expressed as a topcenter or a bottomcenter pos.
        pass

  def build_initial_road(self, player, edge):
    pass

  def build_building(self, building, player, vertex):
    #add has road
    cost = self.building_costs[building]
    new_level = 1 if building == "settlement" else 2
    new_prev_level = 0 if building == "settlement" else 1
    (prev_player, prev_level) = self.buildings[vertex]
    if ((prev_player == player or prev_player == None) and
         prev_level == new_prev_level):
      if (player.has_enough_resources(cost)):
        player.decrement_resources(cost)
        player.settlements.add(vertex)
        self.buildings[vertex] = (player.name, level)
      else:
        raise NotEnoughResources
    else:
      raise CannotBuildThere

  def build_settlement(self, player, vertex):
    self.build_building("settlement", player, vertex)

  def build_city(self, player, vertex):
    self.build_building("city", player, vertex)

  def valid_settlement(self, player, vertex):
    (row, col) = vertex
    if (not self.settup_round):
      pass
      #is_connected
    for dr in xrange(-1, 2, 1):
      for dc in xrange(-1, 2, 1):
        ncol, nrow = (dc + col), (dr + row)
        if ((ncol, nrow) in self.buildings and
             self.buildings[(ncol, nrow)]):
          return False
    return True

  def build_road(self, player, road):
    cost = self.building_costs["road"]
    if (self.roads[road] == None):
      if (player.has_enough_resources(cost)):
        player.decrement_resources(cost)
        player.roads.add(road)
        road_start, road_end = road
        player.roads.add((road_end, road_start))
        self.roads[road] = playe.name
      else:
        raise NotEnoughResources
    elif (self.roads[road] != player.name):
      raise CannotBuildRoadThere

  def build_initial_settlement(self, player, give_resources, vetex, edge):
    (start, end) = edge
    if (not self.valid_settlement):
      raise InvalidSetlement
    elif (start != vertex and end != vertex):
      raise MustConnectRoad
    else:
      self.build_settlement(player, vertex)
      self.build_road(player, edge)
      if give_resource:
        player.give_resource()


  def roll_dice(self):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1+die2
    if (total != 7):
      hexs = self.probabilities[total]
      for h in hexs:
        self.produce_resource(h)
    else:
      pass
      #start move rober

  def produce_resource(self, hex_):
    (col, row) = hex_
    dirs = [(0,0),(1,1),(-1, 1),(1, 2), (-1, 2), (0, 3)]
    valid_vertex = lambda x: x in self.buildings
    get_vertex_contents = lambda x: self.buildings[x]
    not_none = lambda (a, b): a != None
    hex_veticies = map(lambda (a,b):(a+row, b+col), dirs)
    player_verticies = filter(not_none,
                                map(get_vertex_contents,
                                      filter(valid_vertex, hex_veticies)))
    for (player, level) in player_verticies:
      self.players[player].give_resource(resource, level)

  def move_robber(self, player, new_hex):
    current_hex = self.robber_location
    if (current_hex != new_hex):
      robber_location = new_hex
      #steal from a player
    else:
      raise CannotMoveRobberThere
