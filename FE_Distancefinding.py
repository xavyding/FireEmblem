# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:49:37 2018

@author: Yixin Ding
"""

import FE_Pathfinding as Path
import numpy as np

def Distancemap(Map,Pos,Voisinage=float(np.inf)):
    """
    Map à fournir est la matrice d'obstacle (la même que celle qui sera utiliser pour Pathfinding)
    Pos est la position par rapport à laquelle on veut calculer la distance
    
    Cette fonction renvoie une matrice dont les composantes sont les distances par rapport à la position 'Pos'
    (la distance est 'inf' si le déplacement vers cette case est impossible)
    """
   
    DM = np.zeros((np.shape(Map)))
    
    for i in range(np.shape(Map)[0]):
        for j in range(np.shape(Map)[1]):
            if abs(i-Pos[0])+abs(j-Pos[1]) <= Voisinage:
                if Path.find(Map, Pos, (i,j)) == False:
                    DM[i,j] = float(np.inf)
                else:
                    DM[i,j] = len(Path.find(Map, Pos, (i,j)))-1
            else:
                DM[i,j] = float(np.inf)
    return(DM)
            
  

# Test  
if __name__=='__main__':
    Map = np.zeros((5,5))
    Map[1,3] = 1
    Map[2,4] = 1
#    Map[3,2] = 1
    Map[3,1] = 1
    Map[4,2] = 0
    Map[4,0] = 1
    Map[4,3] = 1
    
    Map[2,2] = 0
    Map[1,2] = 1
    Map[0,2] = 0
    
    Pos = (4,2)
#    PosF = (4,1)
    
    Map[PosI[0],PosI[1]] = 88
#    Map[PosF[0],PosF[1]] = 99
    print(Map)
    
#    Chemin = Path.find(Map, PosI, PosF)
#    print('le chemin est:', Chemin)    

    
    print(Distancemap(Map,(Pos),7))
    
