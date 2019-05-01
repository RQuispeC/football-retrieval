import matplotlib
matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt
#import matplotlib.animation as manimation

from sklearn.preprocessing import MinMaxScaler

from football_lib.utils import draw_pitch
from football_lib.utils import general_utils
from football_lib.utils import iotools


# In[2]:

def draw_teams(teamA,teamB):
    fig =plt.figure() #set up the figures
    fig.set_size_inches(7, 5)
    ss = fig.add_subplot(1,1,1)

    ax = draw_pitch.draw_pitch(ss) #overlay our different objects on the pitch

    l, = plt.plot([], [], 'o')
    g, = plt.plot([], [], 'o')

    l.set_data([teamA[0]], [teamA[1]])
    g.set_data([teamB[0]], [teamB[1]])

    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    
    plt.axis('off')

    plt.savefig('rs.png')


def teams(objs):
    #fpath = "/home/leodecio/Área de Trabalho/Unicamp/1st_semester/recuperacao_de_informacao/pesquisa/Dados Futebol/CapBotT1Suav.2d"
    # load data of match
    #ids, objs = read_2d_.read_2d_(fpath)
    
    #Posição do CSV
    X = objs[1][0]
    X[X == -9999.0] = 9999

    Y = objs[1][1]
    Y[Y == -9999.0] = 9999

    new_x = general_utils.rescale(X,122)
    new_y = general_utils.rescale(Y,82)
    
    #np.save("new_x",new_x)
    #np.save("new_y",new_y)

    #definição dos times
    x_1 = new_x[:14]
    x_2 = new_x[14:]

    y_1 = new_y[:14]
    y_2 = new_y[14:]

    return (x_1,y_1),(x_2,y_2)



def main():
    fpath = "/home/leodecio/Área de Trabalho/Unicamp/1st_semester/recuperacao_de_informacao/pesquisa/Dados Futebol/CapBotT1Suav.2d"
    # load data of match
    ids, objs = iotools.read_2d_(fpath)
    teamA,teamB = teams(objs)

    draw_teams(teamA,teamB)

if __name__ == '__main__':
    main()


