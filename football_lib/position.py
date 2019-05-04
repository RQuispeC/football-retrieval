from __future__ import absolute_import

from football_lib import edge_strategies

class Position(object):
  def __init__(self, position_id, team_a, team_b, edge_strategy_name = 'knn', *args, **kwargs):
    self.id = position_id
    self.team_a = team_a
    self.team_b = team_b
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.edges_team_a, self.edges_team_b = self.edge_builder(self)

  def update_edge_strategy(self, edge_strategy_name, *args, **kwargs):
    self.edge_builder = edge_strategies.init_strategy(name = edge_strategy_name, *args, **kwargs)
    self.edges_team_a, self.edges_team_b = self.edge_builder(self)