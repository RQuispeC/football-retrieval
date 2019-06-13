from __future__ import absolute_import

from .player import Player
from .team import Team
from .position import Position
from .utils.iotools import check_isfile

from football_lib import edge_strategies
from football_lib import graph_representation

import numpy as np

import os.path as osp

"""
TODO: 
create function to parse position to file format
create graph_representation that uses the creates THE WHOLE EMBEDDING (calls to graph2vect) in __init__ and then uses the in __call__ just recovers the embeddings, this will require to change _build_match workflow
"""
class Match(object):
  def __init__(self, fpath, edge_strategy_name = 'knn', graph_representation_name = 'space', *args, **kwargs):
    self.id = fpath.split('/')[-1].split('.')[0]
    self.positions = []
    team_size_limit = self._team_partition(fpath)
    print("team size: {}\nReading match data ...".format(team_size_limit))
    self.edge_strategy_name = edge_strategy_name
    self.graph_representation_name = graph_representation_name
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.rep_builder = None
    self._build_match(fpath, team_size_limit, *args, **kwargs)
    print("edges created, computing features")
    self.update_graph_representation(graph_representation_name, *args, **kwargs)
    print("number of positions:", self.size())

  def size(self):
    return len(self.positions)

  def update_edge_strategy(self, edge_strategy_name, *args, **kwargs):
    self.edge_strategy_name = edge_strategy_name
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    for p in self.positions:
      p.update_edge_strategy(self.edge_builder)

  def update_graph_representation(self, graph_representation_name, *args, **kwargs):
    self.graph_representation_name = graph_representation_name
    self.rep_builder = graph_representation.init_representation(name = graph_representation_name, match = self, *args, **kwargs)
    for p in self.positions:
      p.update_graph_representation(self.rep_builder)

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
        p = Position(id_position, team_a, team_b, self.edge_builder, None, *args, **kwargs)
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

  def _convert_to_embedding_format(self, save_dir):
    for p in self.positions:
      fpath  = osp.join(save_dir, "{}.json".format(p.id))
      p._convert_to_embedding_format(fpath)