from __future__ import absolute_import
from __future__ import division

from football_lib.interface.draw import plot_position
from football_lib.match import Match

from football_lib.graph_similarity.player_distance import player_proximity
from football_lib.graph_similarity.position_distance import normal_position_proximity, gaussian_position_proximity, fastdtw_position_proximity

fpath = "data/dados_futebol/CapBotT1Suav.2d"
save_dir = "log/"

# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'space', k = 1)
# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'degree', k = 1)
match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 50)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40)

#distance, path, player_result = player_proximity(match, 5, 'euclidean')
distance, path = fastdtw_position_proximity(match, match)
top = normal_position_proximity(match, match, 50)

print(distance)
print(top)

# plot_position(match[288], save_dir)
# print("Presentation position 288:", match[288].signature)

# match.update_edge_strategy(edge_strategy_name='threshold', thr = 40)
# plot_position(match[289], save_dir)

# match.update_graph_representation(graph_representation_name = 'space', thr = 40)
# plot_position(match[290], save_dir)
# print("Presentation position 288:", match[289].signature)
