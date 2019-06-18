from __future__ import absolute_import
from __future__ import division

import numpy as np

from football_lib.interface.draw import plot_position, plot_comparison, generate_video
from football_lib.match import Match

from football_lib.graph_similarity.player_distance import player_proximity
from football_lib.graph_similarity.team_distance import fastdtw_team_proximity
from football_lib.graph_similarity.position_distance import normal_position_proximity, gaussian_position_proximity, fastdtw_position_proximity

fpath = "/home/vinicius/Documentos/Dados Futebol/teste.2d"
fpath1 = "data/dados_futebol/CapBotT1Suav.2d"
fpath2 = "data/dados_futebol/CapBotT2Suav.2d"
save_dir = "log/"

# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'space', k = 1)
# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'degree', k = 1)
#match = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'degree', thr = 40, sampling = 30, overwrite = False)
match1 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = False, mode = 'team')
match2 = Match(fpath2, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = False, mode = 'team')
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40)

k_allowed = 10

#distance, path, player = player_proximity(match, 6, k_allowed, 'euclidean')

#generate_video(match, match, path, save_dir, match.team_size_limit, match.team_size_limit, 6, 0, player, 0)

# distance, path = fastdtw_position_proximity(match2, match1)
# path = np.array(path)
# print(path.shape)
# print(path[:10])


#import matplotlib.pyplot as plt
#plt.title('similarity over time')
#plt.plot(path[:30, 0], path[:30, 1])
#plt.savefig("tmp.png")

# Position proximity
# top, dis =  normal_position_proximity(match1, match2, 100, 5)
# print(match1.size())
# print(match2.size())

# for i, d in zip(top, dis):
#   print(i, "-->", d)
#   plot_comparison(match1[50], match2[i], save_dir)

# Team proximity
s = match1.get_signature()
s_a = s[:, 1, :]

global_distance, path_res, best_team = fastdtw_team_proximity(s_a, [match2], k_allowed)
print(global_distance)
print(best_team)
generate_video(match1, match2, path_res, save_dir, match1.team_size_limit, match2.team_size_limit)