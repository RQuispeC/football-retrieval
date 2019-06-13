from __future__ import absolute_import

import numpy as np

class Position(object):
  def __init__(self, position_id, team_a, team_b, edge_builder, rep_builder, *args, **kwargs):
    self.id = position_id
    self.team_a = team_a
    self.team_b = team_b
    self.update_edge_strategy(edge_builder)
    self.update_graph_representation(rep_builder)

  def update_edge_strategy(self, edge_builder):
    if edge_builder:
      self.edges_team_a, self.edges_team_b = edge_builder(self)
    else:
      self.edges_team_a, self.edges_team_b = None, None

  def update_graph_representation(self, rep_builder):
    if rep_builder:
      self.signature = rep_builder(self)
    else:
      self.signature = None
  
  def _convert_to_embedding_format(self, fpath):
    f = open(fpath, "w")
    edges = ""
    features = ""
    graph = np.vstack((self.edges_team_a, self.edges_team_b))
    for i, e in enumerate(graph):
      if i > 0:
        edges += ','
        features += ','
      edges += '[{}, {}]'.format(int(e[0]), int(e[1]))
      features += "\"{}\" : \"{}\"".format(i, int(e[2]*10000)) #consider float point values up to 1e4
    f.write("{\"edges\": [" + edges + "], \"features\": {" + features + "}}")
    f.close()