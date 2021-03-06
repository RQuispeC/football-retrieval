from __future__ import absolute_import

from .player import Player
from .team import Team
from .position import Position
from .utils.iotools import check_isfile

from football_lib import edge_strategies
from football_lib import graph_representation

import numpy as np

import os.path as osp

class Match(object):
  def __init__(self, fpath, edge_strategy_name = 'knn', graph_representation_name = 'space', sampling = 1, mode = 'position', *args, **kwargs):
    self.id = fpath.split('/')[-1].split('.')[0]
    self.positions = []
    self.mode = mode
    team_size_limit = self._team_partition(fpath)
    self.team_size_limit = team_size_limit
    print("team size: {}\nReading match data ...".format(team_size_limit))
    self.edge_strategy_name = edge_strategy_name
    self.graph_representation_name = graph_representation_name
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.rep_builder = None
    self._build_match(fpath, team_size_limit, sampling, *args, **kwargs)
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
    if ind < 0 or ind >= self.size():
      raise IndexError("{} not a valid position".format(ind))
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

  def _build_match(self, fpath, team_size_limit, sampling, *args, **kwargs):
    """
    Reads a .2d file and fills self.positions
    """
    check_isfile(fpath)
    self.positions = []
    id_position = 0
    with open(fpath, 'r') as f:
      for ind, ff in enumerate(f):
        if ind % sampling != 0: continue
        _, team_a, team_b = self._token_position(ff, team_size_limit)
        p = Position(id_position, team_a, team_b, self.edge_builder, None, *args, **kwargs)
        self.positions.append(p)
        id_position += 1

  def _team_partition(self, fpath):
    with open(fpath, 'r') as f:
      for ff in f:
        line = np.array(ff.split()).astype(float)
        limit_ind = 0
        cnt = 0
        for i in range(1, len(line), 2):
          if cnt == 11 and line[i] != -9999.0:
            return limit_ind
          if line[i] != -9999.0:
            cnt += 1
          limit_ind += 1

  def _convert_to_embedding_format(self, save_dir):
    for p in self.positions:
      if self.mode == 'position':
        fpath = osp.join(save_dir, "{}.json".format(p.id))
        p._convert_to_embedding_format(fpath, mode = self.mode)
      elif self.mode == 'team':
        fpath1 = osp.join(save_dir, "{}.json".format(p.id * 2))
        fpath2 = osp.join(save_dir, "{}.json".format(p.id * 2 + 1))
        p._convert_to_embedding_format(fpath1, fpath2, mode = self.mode)
      else:
        raise ValueError("{} is not a valid mode".format(self.mode))

  def get_signature(self):
    if self.graph_representation_name != "embedding":
      raise ValueError("this function is available on for signatures embeddings")
    signature = []
    for p in self.positions:
      if self.mode == 'position':
        signature.append(p.signature)
      elif self.mode == 'team':
        team_a_signature, team_b_signature = p.signature
        signature.append([team_a_signature, team_b_signature])
    signature = np.array(signature)
    return signature