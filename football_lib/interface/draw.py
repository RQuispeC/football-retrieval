from __future__ import absolute_import
from __future__ import division

import os
import os.path as osp
import numpy as np

import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
  mpl.use('Agg')
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
from matplotlib import pyplot as plt
import matplotlib.lines as mlines

import gc

from football_lib.utils.iotools import mkdir_if_missing
from football_lib.utils.general_utils import rescale


def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 100, height = 70, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 25.3, fill = False)
    RightPenalty = Rectangle([85.4,22.3], width = 14.6, height = 25.3, fill = False)
    midline = ConnectionPatch([50,0], [50,70], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,26], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([95.1,26], width = 4.9, height = 16, fill = False)

    #Prepare Circles
    centreCircle = plt.Circle((50,35),8.1,color="black", fill = False)
    centreSpot = plt.Circle((50,35),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,35),0.71,color="black")
    rightPenSpot = plt.Circle((90.3,35),0.71,color="black")
    leftArc = Arc((9.7,35),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((90.3,35),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    #return element
    for i in element:
        ax.add_patch(i)
    return ax

def plot_position(position, save_dir):
    team_a_color = 'red'
    team_b_color = 'blue'

    mkdir_if_missing(save_dir)
    fig =plt.figure() #set up the figures
    fig.set_size_inches(7, 5)
    ss = fig.add_subplot(1,1,1)

    #plot background
    ax = draw_pitch(ss) #overlay our different objects on the pitch

    #plot players
    x_pos = rescale(position.team_a.X(), 100)
    y_pos = rescale(position.team_a.Y(), 72)
    l, = plt.plot(x_pos, y_pos, 'o', color=team_a_color)
    x_pos = rescale(position.team_b.X(), 100)
    y_pos = rescale(position.team_b.Y(), 72)
    g, = plt.plot(x_pos, y_pos, 'o', color=team_b_color)

    print('aqui A: ',position.edges_team_a)
    print('aqui B: ',position.edges_team_b)

    #plot edges
    for edge in position.edges_team_a:
        player_m = position.team_a[edge[0]]
        player_n = position.team_a[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_a_color)
        ax.add_line(l)

    for edge in position.edges_team_b:
        player_m = position.team_b[edge[0]]
        player_n = position.team_b[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_b_color)
        ax.add_line(l)

    plt.ylim(-2, 72)
    plt.xlim(-2, 102)
    plt.axis('off')
    plt.savefig(osp.join(save_dir, "{}.png".format(str(position.id).zfill(10))))

    # Clean RAM
    fig.clf()
    plt.close()
    gc.collect()
