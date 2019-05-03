
from scipy.spatial import distance
import numpy as np

#Matrix of distance between images; using euclidean distance
def Matrix_of_distances(team):
    matrix_distances = np.zeros((len(team[0]), len(team[0])))
    merge = []
    for x , y in zip(*team):
        merge.append([x,y])
    for i in range(len(matrix_distances)):
        for j in range(len(matrix_distances[i])):
            matrix_distances[i][j] = distance.euclidean(merge[i], merge[j])
    return matrix_distances


#Sorting distance and only get index
def Matrix_sort_by_index(matrix_distances):
    x_ordenada = np.sort(matrix_distances)
    x = np.argsort(matrix_distances)
    return x

def Get_Pase_corto(team):
    #Distance Team A

    Matrix_of_dist_team = np.zeros((len(team[0]), len(team[0]))).astype(int)

    Position_team = np.zeros((len(team[0]), len(team[0]))).astype(int)

    Matrix_of_dist_team = Matrix_of_distances(team)

    Position_team = Matrix_sort_by_index(Matrix_of_dist_team)

    Dist_to_jugador_mais_proximo_team = Position_team[:,[1]]

    flat_list_team = [item for sublist in Dist_to_jugador_mais_proximo_team for item in sublist]

    #print(flat_list_team)

    return flat_list_team


def Matrix_of_thresold(matrix_distances,threshold):
    posible_pase = []

    pase = []
    print(matrix_distances)

    for i in range(len(matrix_distances)):
        for j in range(len(matrix_distances[i])):
            #print(i,j)
            if matrix_distances[i][j] <= threshold and matrix_distances[i][j] != 0:
                pase.append(j)
                print(matrix_distances[i][j], j)
            #else:
                #pase.append(None)
                #print(matrix_distances[i][j], j)
        #print('Sale', i,j)
        posible_pase.append(pase)
        pase = []
        #print(posible_pase)
        print('Sale')
    print(posible_pase)
    return posible_pase


def Pase_threshold(team,threshold):

    Matrix_of_dist_team = np.zeros((len(team[0]), len(team[0]))).astype(int)

    Position_team = np.zeros((len(team[0]), len(team[0]))).astype(int)

    Matrix_of_dist_team = Matrix_of_distances(team)

    posibles_toques = Matrix_of_thresold(Matrix_of_dist_team, threshold)

    #print(posibles_toques)

    return posibles_toques

    
