import matplotlib
matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt

from sklearn.preprocessing import MinMaxScaler

import general_utils
import iotools

from matplotlib.patches import Arc,Rectangle, ConnectionPatch
from matplotlib import pyplot as plt

def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False)


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    #return element
    for i in element:
        ax.add_patch(i)
        
    return ax


def draw_teams(teamA,teamB,ids_name):
    fig =plt.figure() #set up the figures
    fig.set_size_inches(7, 5)
    ss = fig.add_subplot(1,1,1)

    ax = draw_pitch(ss) #overlay our different objects on the pitch

    l, = plt.plot([], [], 'o')
    g, = plt.plot([], [], 'o')

    l.set_data([teamA[0]], [teamA[1]])
    g.set_data([teamB[0]], [teamB[1]])

    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    
    plt.axis('off')

    plt.savefig('./football_lib/pitch_plots/'+str(ids_name)+'.png')


def teams(objs):
    
    #Posição do CSV

    X = objs[0]
    X[X == -9999.0] = 9999

    Y = objs[1]
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
    
    ## linha 1 do CSV
    teamA,teamB = teams(objs[288])

    draw_teams(teamA,teamB,ids[288])

if __name__ == '__main__':
    main()




