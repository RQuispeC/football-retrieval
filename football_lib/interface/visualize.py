from __future__ import absolute_import
from __future__ import division

import numpy as np

import os.path as osp

import gc
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
  mpl.use('Agg')
import matplotlib.pylab as plt

from football_lib.utils.iotools import mkdir_if_missing


def plot_position(id, players, limit_team, save_dir):
  """
  Plots the positions of a match and save them in save_dir
  """
  mkdir_if_missing(save_dir)
  print(players[0])
  team_a_x, team_a_y = players[:limit_team][0], players[:limit_team][1]
  team_b_x, team_b_y = players[limit_team:][0], players[limit_team:][1]

  # TODO fix this and customize plot to make it look like a football ground
  fig = plt.figure(figsize=(5, 10))
  plt.plot(team_a_x, team_a_y)
  plt.plot(team_b_x, team_b_y)
  plt.axis('off')
  save_name = osp.join(save_dir, "{}.jpg".format(str(id).zfill(9)))
  fig.savefig(save_name, bbox_inches='tight')

  # Clean RAM
  fig.clf()
  plt.close()
  gc.collect()
