from __future__ import absolute_import

import numpy as np

class Team(object):
  def __init__(self, players):
    self.players = players

  def __getitem__(self, player_id):
    for p in self.players:
      if p.id  == player_id:
        return p
    raise IndexError("Player {} does not exits in team {}".format(player_id, self.id()))

  def size(self):
    return len(self.players)

  def ID(self):
    ids = []
    for p in self.players:
      ids.append(p.id)
    ids = np.array(ids)
    return ids

  def X(self):
    xs = []
    for p in self.players:
      xs.append(p.x)
    xs = np.array(xs)
    return xs

  def Y(self):
    ys = []
    for p in self.players:
      ys.append(p.y)
    ys = np.array(ys)
    return ys