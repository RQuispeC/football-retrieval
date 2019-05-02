#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib
matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as manimation


from sklearn.preprocessing import MinMaxScaler
from skimage.exposure import rescale_intensity

from football_lib.utils import draw_pitch


# In[4]:


def token_position(position_str):
    position = position_str.split()#.astype(float)
    id_position = int(position[0])
    players_x = []
    players_y = []
    for i in range(1, len(position), 2):
        players_x.append(position[i])
        players_y.append(position[i + 1])
        
    players_x = np.array(players_x).astype('float')
    players_y = np.array(players_y).astype('float')
    return id_position, players_x,players_y


# In[5]:


def read_2d(fpath):
    """
    Reads a .2d file
    Input
    
    fpath: file path of .2d 
    
    Ouput:
    ids: list of times (e.g. [1, 2, ... , n])
    objs: list of 2 dimention files (shape = (n, k, 2)) k is the number of players
    """
    #check_isfile(fpath)
    objs = []
    ids = []
    with open(fpath, 'r') as f:
        for ff in f:
            id_position, players_x, players_y = token_position(ff)
            objs.append((players_x, players_y))
            ids.append(id_position)
    objs = np.array(objs)
    ids = np.array(ids)
    return ids, objs


# In[6]:


def rescale(image,intensity):
    output = rescale_intensity(image, in_range=(0, intensity))
    output = (output * intensity).astype("float")
    return output


# In[7]:


FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)


# In[8]:


fpath = "/home/vinicius/Documentos/Dados Futebol/CapBotT1Suav.2d"
# load data of match
ids, objs = read_2d(fpath)


# In[9]:


X = objs[130][0]
X[X == -9999.0] = 9999

Y = objs[130][1]
Y[Y == -9999.0] = 9999


# In[10]:


new_x = rescale(X,122)
new_y = rescale(Y,82)

#np.save("new_x",new_x)
#np.save("new_y",new_y)


# In[11]:


fig =plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ss = fig.add_subplot(1,1,1)

ax = draw_pitch.draw_pitch(ss) #overlay our different objects on the pitch

l, = plt.plot([], [], 'o')
g, = plt.plot([], [], 'o')

plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')


# In[13]:


#definição dos times
x_1 = new_x[:14]
x_2 = new_x[14:]

y_1 = new_y[:14]
y_2 = new_y[14:]


# In[15]:


with writer.saving(fig, "g1.mp4", 100):
    for i in range(0,len(new_x)):
        l.set_data([x_1], [y_1])
        g.set_data([x_2], [y_2])
        writer.grab_frame()


# In[ ]:




