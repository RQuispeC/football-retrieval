from __future__ import absolute_import

from .player import Player
from .team import Team
from .position import Position
from .utils.iotools import check_isfile

import numpy as np

class Match(object):
  def __init__(self, fpath, edge_strategy_name = 'knn', *args, **kwargs):
    self.positions = []
    team_size_limit = self._team_partition(fpath)
    print("team size: {}\nReading match data ...".format(team_size_limit))
    self.edge_strategy_name = edge_strategy_name
    self._build_match(fpath, team_size_limit, *args, **kwargs)
    print("number of positions:", self.size())

  def size(self):
    return len(self.positions)
  
  def update_edge_strategy(self, new_edge_strategy, *args, **kwargs):
    self.edge_strategy_name = new_edge_strategy
    for p in self.positions:
      p.update_edge_strategy(new_edge_strategy, *args, **kwargs)

  def __getitem__(self, ind):
    if ind < 0 or ind > self.size():
      raise IndexError("{} out of range (0, {})".format(ind, self.size - 1))
    return self.positions[ind]

  def _token_position(self, position_str, team_size_limit):
    position = np.array(position_str.split()).astype(float)
    id_position = int(position[0])
    players_team_a = []
    players_team_b = []
    for player_id, i in enumerate(range(1, len(position), 2)):
      if position[i] == -9999.0: continue
      p = Player(player_id, x = position[i], y = position[i + 1])
      if player_id < team_size_limit:
        players_team_a.append(p)
      else:
        players_team_b.append(p)
    team_a = Team(players = players_team_a)
    team_b = Team(players = players_team_b)
    return id_position, team_a, team_b

  def _build_match(self, fpath, team_size_limit, *args, **kwargs):
    """
    Reads a .2d file and fills self.positions
    """
    check_isfile(fpath)
    self.positions = []
    with open(fpath, 'r') as f:
      for ff in f:
        id_position, team_a, team_b = self._token_position(ff, team_size_limit)
        p = Position(id_position, team_a, team_b, self.edge_strategy_name, *args, **kwargs)
        self.positions.append(p)

  def _team_partition(self, fpath):
    with open(fpath, 'r') as f:
      for ff in f:
        line = np.array(ff.split()).astype(float)
        flag = False
        limit_ind = 0
        for i in range(1, len(line), 2):
          if line[i] == -9999.0:
            flag = True
          if flag and line[i] != -9999.0:
            return limit_ind
          limit_ind += 1
