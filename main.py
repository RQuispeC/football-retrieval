from __future__ import absolute_import
from __future__ import division

import numpy as np

from football_lib.interface.draw import plot_position, plot_comparison, generate_video
from football_lib.match import Match

from football_lib.graph_similarity.player_distance import player_proximity
from football_lib.graph_similarity.team_distance import fastdtw_team_proximity
from football_lib.graph_similarity.position_distance import normal_position_proximity, gaussian_position_proximity, fastdtw_position_proximity

fpath = "/home/vinicius/Documentos/Dados Futebol/teste.2d"
fpath1 = "/home/vinicius/Documentos/Dados Futebol/CapBotT1Suav.2d"
fpath2 = "/home/vinicius/Documentos/Dados Futebol/CapBotT2Suav.2d"
fpath3 = "/home/vinicius/Documentos/Dados Futebol/CapPalT1Suav.2d"
fpath4 = "/home/vinicius/Documentos/Dados Futebol/CapSpoT1Suav.2d"
fpath5 = "/home/vinicius/Documentos/Dados Futebol/SpoFlaT1Suav.2d"
save_dir = "/home/vinicius/Documentos/log/"

samp = 20

# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'space', k = 1)
# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'degree', k = 1)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'degree', thr = 40, sampling = 10, overwrite = False) # correto
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'eccentricity', thr = 40, sampling = 10, overwrite = False) # correto
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40, sampling = samp, overwrite = False) # correto
# match1 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = False)
# match2 = Match(fpath2, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40, sampling = 10, overwrite = False)
# match1 = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'eccentricity', thr = 40, sampling = 40, overwrite = False)
match = Match(fpath1, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40, sampling = 40, overwrite = False)
match1 = Match(fpath3, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40, sampling = 40, overwrite = False)
match2 = Match(fpath4, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40, sampling = 40, overwrite = False)
match3 = Match(fpath5, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40, sampling = 40, overwrite = False)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'embedding', thr = 40)
# match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'gEfficiency', thr = 40)

# for i in match[0].team_a.players:
# 	print(i.id)

# print(len(match[0].team_a.players))

k_allowed = 5
player_query = 6
team_query = 0

matches = [match1,match2,match3]

distance, path, player, match_ = player_proximity(match, matches, player_query, k_allowed, 'euclidean')

print(distance, player, match_)


match_res = 0
if player >= matches[match_].team_size_limit:
	match_res = 1

if(match_ == 0):
	generate_video(match, match1, path, samp, save_dir, match.team_size_limit, match1.team_size_limit, player_query, team_query, player, match_res)
elif(match_ == 1):
	generate_video(match, match2, path, samp, save_dir, match.team_size_limit, match2.team_size_limit, player_query, team_query, player, match_res)
else:
	generate_video(match, match3, path, samp, save_dir, match.team_size_limit, match3.team_size_limit, player_query, team_query, player, match_res)

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
# s = match1.get_signature()
# s_a = s[:, 1, :]

# global_distance, path_res, best_team = fastdtw_team_proximity(s_a, [match2])
# print(global_distance)
# print(best_team)