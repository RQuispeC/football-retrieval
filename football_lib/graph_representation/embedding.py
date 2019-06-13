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
  def __init__(self, match, *args, **kwargs):
    mkdir_if_missing("football_lib/graph_representation/graph2vec/dataset")
    mkdir_if_missing("football_lib/graph_representation/graph2vec/features")
    input_path = osp.join("football_lib/graph_representation/graph2vec/dataset", match.id)
    output_path = osp.join("football_lib/graph_representation/graph2vec/features", "{}.csv".format(match.id))
    mkdir_if_missing(input_path)
    match._convert_to_embedding_format(input_path)
    command = "python3 football_lib/graph_representation/graph2vec/src/graph2vec.py --input-path {}/ --output-path {}".format(input_path, output_path)
    print("Executing", command)
    os.system(command)
    csv = pd.read_csv(output_path) 
    self.features = {int(row[0]): row[1:] for row in np.array(csv)}

  def __call__(self, position):
    return self.features[position.id]