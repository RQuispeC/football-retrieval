from __future__ import absolute_import

import os
import os.path as osp
import errno
import json
import shutil
import numpy as np

def mkdir_if_missing(directory):
  if not osp.exists(directory):
    try:
      os.makedirs(directory)
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise


def check_isfile(path):
  isfile = osp.isfile(path)
  if not isfile:
    print("=> Warning: no file found at '{}' (ignored)".format(path))
  return isfile


def read_json(fpath):
  with open(fpath, 'r') as f:
    obj = json.load(f)
  return obj

def token_position(position_str):
  position = position_str.split().astype(float)
  id_position = int(position[0])
  players = []
  for i in range(1, len(position), 2):
    players.append(position[i], position[i + 1])
  players = np.array(players)
  return id_position, players
  
def read_2d(fpath):
  """
  Reads a .2d file

  Input
  
  fpath: file path of .2d 

  Ouput:

  ids: list of times (e.g. [1, 2, ... , n])
  objs: list of 2 dimention files (shape = (n, k, 2)) k is the number of players
  """
  check_isfile(fpath)
  objs = []
  ids = []
  with open(fpath, 'r') as f:
    for ff in f:
      id_position, players = token_position(ff)
      objs.append(players)
      ids.append(id_position)
  objs = np.array(objs)
  ids = np.array(ids)
  return ids, objs

def write_json(obj, fpath):
  mkdir_if_missing(osp.dirname(fpath))
  with open(fpath, 'w') as f:
    json.dump(obj, f, indent=4, separators=(',', ': '))