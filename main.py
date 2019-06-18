from __future__ import absolute_import
from __future__ import division

import numpy as np

from football_lib.interface.draw import plot_position, plot_comparison
from football_lib.match import Match

from football_lib.graph_similarity.player_distance import player_proximity
from football_lib.graph_similarity.position_distance import normal_position_proximity, gaussian_position_proximity, fastdtw_position_proximity

fpath1 = "data/dados_futebol/CapBotT1Suav.2d"
fpath2 = "data/dados_futebol/CapBotT2Suav.2d"
save_dir = "log/"

# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'space', k = 1)
# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'degree', k = 1)
#match = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'degree', thr = 40, sampling = 50, overwrite = False)
match1 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 50, overwrite = True)
match2 = Match(fpath2, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 50, overwrite = True)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40)

#distance, path = fastdtw_position_proximity(match2, match1)
#path = np.array(path)
#print(path.shape)
#print(path[:10])


#import matplotlib.pyplot as plt
#plt.title('similarity over time')
#plt.plot(path[:30, 0], path[:30, 1])
#plt.savefig("tmp.png")

top, dis =  normal_position_proximity(match1, match2, 100, 5)
print(match1.size())
print(match2.size())

for i, d in zip(top, dis):
  print(i, "-->", d)
  plot_comparison(match1[50], match2[i], save_dir)

# plot_position(match[288], save_dir)
# print("Presentation position 288:", match[288].signature)

# match.update_edge_strategy(edge_strategy_name='threshold', thr = 40)
# plot_position(match[289], save_dir)

# match.update_graph_representation(graph_representation_name = 'space', thr = 40)
# plot_position(match[290], save_dir)
# print("Presentation position 288:", match[289].signature)
