from __future__ import absolute_import
from __future__ import division

from football_lib.interface.visualize import plot_position
from football_lib.utils.iotools import read_2d

fpath = "data/data/dados_futebol/CapBotT1Suav.2d"
save_dir = "log/CapBotT1Suav"

# load data of match
ids, objs = read_2d(fpath)

# TODO: separate teams based on 9999.000 position on first frame
limit_team = 14 #change this

for id_position, players in zip(ids, objs):
  plot_position(id_position, players, limit_team, save_dir)
