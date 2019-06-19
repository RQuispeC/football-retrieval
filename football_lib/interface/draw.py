from __future__ import absolute_import
from __future__ import division

import os
import os.path as osp
import numpy as np

import subprocess
import glob
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
  mpl.use('Agg')
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
    save_path = osp.join(save_dir, "{}.png".format(str(position.id).zfill(10)))
    plt.savefig(save_path)

    # Clean RAM
    fig.clf()
    plt.close()
    gc.collect()
    return save_path


def plot_comparison(i, t1, t2, position_a, position_b, save_dir, team1_size_limit, team2_size_limit, player_query = -1, query_team = -1, player_res = -1, res_team = -1, save_plot = True):
    team_a_color = 'red'
    team_b_color = 'green'
    player_color = 'blue'

    mkdir_if_missing(save_dir)
    fig =plt.figure() #set up the figures
    fig.set_size_inches(14, 5)
    ss1 = fig.add_subplot(1,2,1)
    title_ = 'Time (seconds): ' + str(t1)
    plt.title(title_,loc='left')

    #plot background
    ax1 = draw_pitch(ss1) #overlay our different objects on the pitch

    #plot players
    x_pos = rescale(position_a.team_a.X(), 100)
    y_pos = rescale(position_a.team_a.Y(), 72)
    l, = plt.plot(x_pos, y_pos, 'o', color=team_a_color)

    if query_team == 0:
        if player_query >= 11:
            x_query = x_pos[player_query-11]
            y_query = y_pos[player_query-11]
        else:
            x_query = x_pos[player_query]
            y_query = y_pos[player_query]
        l, = plt.plot(x_query, y_query, 'o', color=player_color)

    x_pos = rescale(position_a.team_b.X(), 100)
    y_pos = rescale(position_a.team_b.Y(), 72)
    g, = plt.plot(x_pos, y_pos, 'o', color=team_b_color)

    if query_team == 1:
        if player_query >= 11:
            x_query = x_pos[player_query-11]
            y_query = y_pos[player_query-11]
        else:
            x_query = x_pos[player_query]
            y_query = y_pos[player_query]
        g, = plt.plot(x_query, y_query, 'o', color=player_color)

    #plot edges
    for edge in position_a.edges_team_a:
        player_m = position_a.team_a[edge[0]]
        player_n = position_a.team_a[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_a_color)
        if query_team == 0 and (player_m.id == player_query or player_n.id == player_query):
            l = mlines.Line2D(x_pos, y_pos, color=player_color)
        ax1.add_line(l)

    for edge in position_a.edges_team_b:
        player_m = position_a.team_b[edge[0]]
        player_n = position_a.team_b[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_b_color)
        if query_team == 1 and (player_m.id == player_query + team1_size_limit or player_n.id == player_query + team1_size_limit):
            l = mlines.Line2D(x_pos, y_pos, color=player_color)
        ax1.add_line(l)

    plt.ylim(-2, 72)
    plt.xlim(-2, 102)
    plt.axis('off')

    ss2 = fig.add_subplot(1,2,2)
    ax2 = draw_pitch(ss2) #overlay our different objects on the pitch
    title_ = 'Time (seconds): ' + str(t2)
    plt.title(title_,loc='left')
    
    #plot players
    x_pos = rescale(position_b.team_a.X(), 100)
    y_pos = rescale(position_b.team_a.Y(), 72)
    l, = plt.plot(x_pos, y_pos, 'o', color=team_a_color)

    if res_team == 0:
        if player_res >= 11:
            x_res = x_pos[player_res-11]
            y_res = y_pos[player_res-11]
        else:
            x_res = x_pos[player_res]
            y_res = y_pos[player_res]
        l, = plt.plot(x_res, y_res, 'o', color=player_color)

    x_pos = rescale(position_b.team_b.X(), 100)
    y_pos = rescale(position_b.team_b.Y(), 72)
    g, = plt.plot(x_pos, y_pos, 'o', color=team_b_color)

    if res_team == 1:
        if player_res >= 11:
            x_res = x_pos[player_res-11]
            y_res = y_pos[player_res-11]
        else:
            x_res = x_pos[player_res]
            y_res = y_pos[player_res]
        g, = plt.plot(x_res, y_res, 'o', color=player_color)


    #plot edges
    for edge in position_b.edges_team_a:
        player_m = position_b.team_a[edge[0]]
        player_n = position_b.team_a[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_a_color)
        if res_team == 0 and (player_m.id == player_res or player_n.id == player_res):
            l = mlines.Line2D(x_pos, y_pos, color=player_color)
        ax2.add_line(l)

    for edge in position_b.edges_team_b:
        player_m = position_b.team_b[edge[0]]
        player_n = position_b.team_b[edge[1]]
        x_pos = rescale(np.array([player_m.x, player_n.x]), 100)
        y_pos = rescale(np.array([player_m.y, player_n.y]), 72)
        l = mlines.Line2D(x_pos, y_pos, color=team_b_color)
        if res_team == 1 and (player_m.id == player_res - team2_size_limit or player_n.id == player_res):
            l = mlines.Line2D(x_pos, y_pos, color=player_color)
        ax2.add_line(l)

    plt.ylim(-2, 72)
    plt.xlim(-2, 102)
    plt.axis('off')

    save_path = save_dir + "file%08d.png" % i
    if save_plot:
        plt.savefig(save_path)
        # plt.savefig(osp.join(save_dir, "{}_{}.png".format(str(position_a.id).zfill(10), str(position_b.id).zfill(10))))
    #convert to image
    #canvas = FigureCanvas(fig)
    #canvas.draw()
    #s, (width, height) = canvas.print_to_buffer()
    #image = np.fromstring(s, np.uint8).reshape((height, width, 4))

    # Clean RAM
    fig.clf()
    plt.close()
    gc.collect()

    return save_path

def generate_video(match1, match2, path, sampling, save_dir, team1_size_limit, team2_size_limit, player_query = -1, query_team = -1, player_res = -1, res_team = -1):
    for i in range(path.shape[0]):
        p1 = path[i,0]
        p2 = path[i,1]

        t1 = round((p1 * sampling) / 30.0)
        t2 = round((p2 * sampling) / 30.0)

        plot_comparison(i, t1, t2, match1[p1], match2[p2], save_dir, team1_size_limit, team2_size_limit, player_query, query_team, player_res, res_team)

    os.chdir(save_dir)

    name = match1.id + '_' + match2.id + '_' + str(player_query) + '_' + str(query_team) + '_' + str(player_res) + '_' + str(res_team) + '.mp4'

    subprocess.call([
        'ffmpeg', '-framerate', '2', '-i', 'file%08d.png', '-r', '30', '-pix_fmt', 'yuv420p',
        name
    ])

    for file_name in glob.glob("*.png"):
        os.remove(file_name)

    return save_dir+name