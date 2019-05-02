from __future__ import absolute_import
from __future__ import division

from football_lib.interface.visualize import plot_position
from football_lib.interface.draw import generate_figures
from football_lib.utils.iotools import read_2d

# fpath = "data/data/dados_futebol/CapBotT1Suav.2d"
fpath = "/home/vinicius/Documentos/Dados Futebol/CapBotT1Suav.2d"
# save_dir = "log/CapBotT1Suav"
save_dir = "/home/vinicius/Documentos/log/"

# load data of match
ids, objs = read_2d(fpath)

# TODO: separate teams based on 9999.000 position on first frame
limit_team = 14 #change this

# import os
# print(os.getcwd())

for id_position, players in zip(ids, objs):
  generate_figures(id_position,players,save_dir)
  break