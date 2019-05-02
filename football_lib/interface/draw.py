import sys
sys.path.insert(0,sys.path[0] + '/football_lib/utils')

import general_utils

import numpy as np

from matplotlib.patches import Arc, Rectangle, ConnectionPatch
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


def draw_teams(teamA,teamB,ids_name,path_save):
    fig =plt.figure() #set up the figures
    fig.set_size_inches(7, 5)
    ss = fig.add_subplot(1,1,1)

    ax = draw_pitch(ss) #overlay our different objects on the pitch

    l, = plt.plot(teamA[0], teamA[1], 'o', color='red')
    g, = plt.plot(teamB[0], teamB[1], 'o', color='black')

    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    
    plt.axis('off')

    plt.savefig(path_save+str(ids_name)+'.png')


def teams(players,limit):
    X = players[:,0]
    Y = players[:,1]
    
    X_temp= X[:limit]
    sum_ = np.sum(X_temp == -9999.0)

    X = X[X != -9999.0]
    Y = Y[Y != -9999.0]

    X = general_utils.rescale(X,122)
    Y = general_utils.rescale(Y,82)

    limit = limit - sum_

    team_a_x, team_a_y = X[:limit], Y[:limit]
    team_b_x, team_b_y = X[limit:], Y[limit:]

    return (team_a_x,team_a_y),(team_b_x,team_b_y)

def partition(line):
    flag = False
    for i in range(len(line)):
        if line[i][0] == -9999.0:
            flag = True
        if flag and line[i][0] != -9999.0:
            return i

def generate_figures(ids, objs, path_save):
    limit = partition(objs)
    teamA,teamB = teams(objs,limit)
    draw_teams(teamA,teamB,ids,path_save)