from __future__ import absolute_import
from __future__ import division

from football_lib.utils.edgestools import dist_mat

import numpy as np
import os
import os.path as osp
import pandas as pd

from football_lib.utils.iotools import mkdir_if_missing

__all__ =  ['Embedding']

class Embedding(object):
  def __init__(self, match, overwrite = False, *args, **kwargs):
    dataset_path = "football_lib/graph_representation/graph2vec/dataset"
    feature_path = "football_lib/graph_representation/graph2vec/features"
    input_path = osp.join(dataset_path, match.id)
    output_path = osp.join(feature_path, "{}.csv".format(match.id))
    if not osp.exists(input_path) or not osp.exists(output_path) or overwrite:
      mkdir_if_missing(dataset_path)
      mkdir_if_missing(feature_path)
      mkdir_if_missing(input_path)
      match._convert_to_embedding_format(input_path)
      command = "python3 football_lib/graph_representation/graph2vec/src/graph2vec.py --input-path {}/ --output-path {}".format(input_path, output_path)
      print("Executing", command)
      os.system(command)
    else:
      print("Recovering pre-calculated features")
    csv = pd.read_csv(output_path) 
    self.features = {int(row[0]): row[1:] for row in np.array(csv)}

  def __call__(self, position):
    return self.features[position.id]