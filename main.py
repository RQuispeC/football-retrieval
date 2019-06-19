from __future__ import absolute_import
from __future__ import division

import numpy as np

from football_lib.interface.draw import plot_position, plot_comparison, generate_video
from football_lib.match import Match

from football_lib.graph_similarity.player_distance import player_proximity
from football_lib.graph_similarity.team_distance import fastdtw_team_proximity
from football_lib.graph_similarity.position_distance import normal_position_proximity, gaussian_position_proximity, fastdtw_position_proximity


fpath0 = "data/dados_futebol/CapBotT1Suav.2d"
fpath1 = "data/dados_futebol/CapBotT1Suav.2d"
fpath2 = "data/dados_futebol/CapBotT2Suav.2d"
fpath3 = "data/dados_futebol/CapSpoT1Suav.2d"
fpath4 = "data/dados_futebol/CapSpoT2Suav.2d"
save_dir = "log/"

match0 = Match(fpath1, edge_strategy_name='knn', graph_representation_name = 'degree', k = 40, sampling = 10)
match1 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = True, mode = 'position')
match2 = Match(fpath2, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = True, mode = 'position')
match3 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = True, mode = 'team')
match4 = Match(fpath2, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = True, mode = 'team')

#plot a position
plot_position(match0[100], save_dir)

# Player similarity
k_allowed = 5
player_query = 6
distance, path, best_player = player_proximity(match0, player_query, k_allowed, 'euclidean')
generate_video(match0, match0, path, save_dir, match0.team_size_limit, match0.team_size_limit, player_query, 0, best_player, 0)

# Position proximity
query = 100
top_size = 5
top, dis =  normal_position_proximity(match1, match2, query, top_size)
for ind, (i, d) in enumerate(zip(top, dis)):
  print(i, "-->", d)
  plot_comparison(ind, match1[query], match2[i], save_dir, match1.team_size_limit, match2.team_size_limit)

# Team proximity
s = match3.get_signature()
team = 0
s_a = s[:, team, :]
k_allowed = 3
global_distance, path, best_team = fastdtw_team_proximity(s_a, [match4], k_allowed)
print(global_distance)
print(best_team)
generate_video(match1, match2, path, save_dir, match3.team_size_limit, match4.team_size_limit)
