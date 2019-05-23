from __future__ import absolute_import
from __future__ import division

from football_lib.interface.draw import plot_position
from football_lib.match import Match

fpath = "/home/vinicius/Documentos/Dados Futebol/CapBotT1Suav.2d"
save_dir = "/home/vinicius/Documentos/log"

# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'space', k = 1)
# match = Match(fpath, edge_strategy_name='knn', graph_representation_name = 'degree', k = 1)
match = Match(fpath, edge_strategy_name='threshold', graph_representation_name = 'eccentricity', thr = 40)
plot_position(match[288], save_dir)
# print("Presentation position 288:", match[288].signature)

# match.update_edge_strategy(edge_strategy_name='threshold', thr = 40)
# plot_position(match[289], save_dir)

# match.update_graph_representation(graph_representation_name = 'space', thr = 40)
# plot_position(match[290], save_dir)
# print("Presentation position 288:", match[289].signature)
