from __future__ import absolute_import

from football_lib import edge_strategies
from football_lib import graph_representation

class Position(object):
  def __init__(self, position_id, team_a, team_b, edge_strategy_name = 'knn', graph_representation_name = 'space', *args, **kwargs):
    self.id = position_id
    self.team_a = team_a
    self.team_b = team_b
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.edges_team_a, self.edges_team_b = self.edge_builder(self)
    self.rep_builder = graph_representation.init_representation(name = graph_representation_name, *args, **kwargs)
    self.signature = self.rep_builder(self)

  def update_edge_strategy(self, edge_strategy_name, *args, **kwargs):
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.edges_team_a, self.edges_team_b = self.edge_builder(self)

  def update_graph_representation(self, graph_representation_name, *args, **kwargs):
    self.rep_builder = graph_representation.init_representation(name = graph_representation_name, *args, **kwargs)
    self.signature = self.rep_builder(self)
