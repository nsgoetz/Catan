
import random

class Player(object):

  def __init__(self, name, color):
    self.name = name
    self.color = color
    self.resources = {}
    self.cities = set()
    self.settlements = set()
    self.roads = set()
    self.devcards = {}
    self.cities_left = 4
    self.settlements_left = 5
    self.roads_left = 15
    self.largest_army = False
    self.knights_played = 0
    self.longest_road = False
    self.longest_road_len = 0
    #dev card played this turn

  def victory_points(self):
    vp = len(self.settlements) + (len(self.cities)*2)
    if self.largest_army:
      vp += 2
    if self.longest_road:
      vp += 2
    if ("victory_point" in self.devcards):
      vp += self.devcards["victory_point"]
    return vp

  def give_resource(self, resource, amount = 1):
    if (resource not in self.resources):
      self.resources[resource] = 0
    self.resources[resource] = self.resources[resource] + 1

  def give_devcards(self, devcard):
    if (devcards not in self.devcards):
      self.devcards[devcard] = 0
    self.devcards[devcard] = self.devcards[devcard] + 1

  def has_enough_resources(self, resource_dict):
    for (resouce, needed) in resource_dict:
      #can it be none?
      if ((self.resources[resource] == None) or
          (self.resources[resource] < needed)):
        return False
    return True

  def decrement_resources(self, resource_dict):
    if (not has_enough_resources(resource_dict)):
      raise NotEnoughResources
    else:
      for (resouce, dec) in resource_dict:
        self.resources[resouce] -= dec

  def find_longest_path_length(self):
    pass


class Board(object):

  def __init__(self):
    #self.robber_location =
    #edges don't exist until we build them? or not.
    #build board
    #define a hex by the top vertex
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
    self.largest_army_player = None
    self.longest_road_player = None
    self.longest_road_len = None
    self.settup_round = True
    #resouces left?

  def make_possible_buildings(self):
    rows, cols = self.vertex_rows, self.vertex_cols
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
            self.buildings[(col, row)] = (None, 0)

  def make_hexes(self):
    resources = (["brick",  "ore"] * 3) + (["lumber", "wool", "grain"] * 4) + ["desert"]
    p_distribution = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    for p in xrange(2,13):
      self.probabilities[p] = []
    fake_tops = set([(0,5), (1,3), (2,1), (8,1), (9,3), (10, 5)])
    for (col, row) in self.buildings:
      if ((row % 2 == 1) and ((col-1, row-1) in self.buildings) and
          ((col+1, row-1) in self.buildings) and (col, row-3) in self.buildings):
        if (len(resources) == 0):
          raise InsufficientResources
        else:
          rand_resource_index = random.randint(0, len(resources)-1)
          resource = resources.pop(rand_resource_index)
          if (resource == "desert"):
            self.hexes[(col, row)] = (resource, None)
            self.robber_location = (col, row)
          else:
            if (len(p_distribution) == 0):
              raise InsufficientProbabilities
            else:
              rand_p_index = random.randint(0, len(p_distribution)-1)
              probability = p_distribution.pop(rand_p_index)
              self.hexes[(col, row)] = (resource, probability)
              self.probabilities[probability].append((col, row))
    #if adjacent red probabilities = start over
    if ((len(resources) != 0) or (len(p_distribution) != 0)):
        raise InsufficientHexes

  def make_possible_roads(self):
    self.edges = {} #((row1, col1), (row2, col2)) -> owner (defualt None, (row1 < row2))
    dirs = [(1,0), (1, 1), (1, -1)]
    for (r, c) in self.buildings:
      for (dr, dc) in dirs:
        r2, c2 = r+dr, c+dc
        if (r2, c2) in self.buildings:
          self.roads[((r,c), (r2, c2))] = None

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



class GameController(object):

  def __init__(self, players):
    self.players = [Player(p) for p in players]
    self.board = Board()

  def end_round_number(self):
    pass

b = Board()