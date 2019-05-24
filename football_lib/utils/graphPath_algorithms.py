import sys
import numpy as np

def floyd_warshall(graph):
    dist = graph.copy()

    v = graph.shape[0]

    for k in range(v):
        for i in range(v):
            for j in range(v):
                if dist[i,k] + dist[k,j] < dist[i,j]: 
                    dist[i,j] = dist[i,k] + dist[k,j]

    return dist    

def minDistance(dist, V, sptSet): 
    minimum = sys.maxint 
    for v in range(V): 
        if dist[v] < minimum and sptSet[v] == False: 
            minimum = dist[v] 
            min_index = v 
    return min_index

def dijkstra(g,V,src = 0):
    graph = g.copy()
    dist = [sys.maxint] * V 
    dist[src] = 0
    sptSet = [False] * V 
    for cout in range(V): 
        u = minDistance(dist, V, sptSet) 
        sptSet[u] = True
        
        for v in range(V): 
            if(graph[u][v] > 0 and sptSet[v] == False
                and dist[v] > dist[u] + graph[u][v]): 
                    dist[v] = dist[u] + graph[u][v]
    
    return np.asarray(dist)
