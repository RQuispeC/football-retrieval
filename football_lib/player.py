from __future__ import absolute_import

class Player(object):
  def __init__(self, player_id, x, y):
    self.id = player_id
    self.x = x
    self.y = y

  def __eq__(self, other):
    return (isinstance(other, type(self)) and (self.y, self.x) == (other.y, other.x))

  def __hash__(self):
    return (hash(self.x) ^ hash(self.y))