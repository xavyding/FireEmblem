# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 14:06:54 2018

@author: YIXIN DING
TUTO: https://www.youtube.com/watch?v=KNXfSOx4eEE
"""

import numpy as np


def find(Map, PosI, PosF):
    """
    La variable 'Map', est une matrice de 0 et de 1 codant la carte d'obstacle. Les 0 sont les cases valides, et les 1 sont les cases impassables
    Les variables 'PosI' et 'PosF' sont la positions initiale (indice matrice) et la position finale.
    
    Cette fonction retourne soit False s'il n'existe pas de chemin possible entre 'PosI' et 'PosF', soit le chemin le plus court reliant ces deux postions.
    """
    
   # Pour les tests, cf. Pathfinding et Pathfinding2 
    
    InitialPosI = PosI
    InitialPosF = PosF
    Chemin = []
    
    Hvalue = np.zeros((np.shape(Map))) #Distance
    Gvalue = np.zeros((np.shape(Map))) #Movement Cost
    Fvalue = np.zeros((np.shape(Map))) #G+H    
    Gvalue[:] = np.nan #initialiser Gvalue à une matrice NaN
    
    OpenList = [(InitialPosI,'N')]
    CloseList = []
    
    # Initialisation de Hvalue
    for i in range(np.shape(Hvalue)[0]):
        for j in range(np.shape(Hvalue)[1]):
            if Map[i,j] !=1:
                Hvalue[i,j] = abs(i-PosF[0]) + abs(j-PosF[1])
            else:
                Hvalue[i,j] = np.nan

### Round 1 (+initialisations)
        
    CloseList.append(tuple(PosI))
    
    if PosI[0]-1>=0 and Map[PosI[0]-1,PosI[1]] != 1 and ((PosI[0]-1,PosI[1]) not in OpenList) and ((PosI[0]-1,PosI[1]) not in CloseList):  #Check vertical haut
        OpenList.append(((PosI[0]-1,PosI[1]),'D'))     #D : fleche vers le bas..
    if PosI[0]+1<=np.shape(Map)[0]-1 and Map[PosI[0]+1,PosI[1]] != 1 and ((PosI[0]+1,PosI[1]) not in OpenList) and ((PosI[0]+1,PosI[1]) not in CloseList): #Check vertical bas
        OpenList.append(((PosI[0]+1,PosI[1]),'U'))        
    if PosI[1]-1>=0 and Map[PosI[0],PosI[1]-1] != 1 and ((PosI[0],PosI[1]-1) not in OpenList) and ((PosI[0],PosI[1]-1) not in CloseList): #Check horiz gauche
        OpenList.append(((PosI[0],PosI[1]-1),'R'))
    if PosI[1]+1<=np.shape(Map)[1]-1 and Map[PosI[0],PosI[1]+1] != 1 and ((PosI[0],PosI[1]+1) not in OpenList) and ((PosI[0],PosI[1]+1) not in CloseList): #Check horiz droit
        OpenList.append(((PosI[0],PosI[1]+1),'L'))
    
    
    for OV in OpenList: #OV pour OpenValue 
        Gvalue[OV[0][0],OV[0][1]] = 10
        
    Fvalue = np.copy(Gvalue + Hvalue)
    for CV in CloseList: #CV pour ClosedValue
        Fvalue[CV[0],CV[1]] = np.nan
        

#### Round NEXT    
    ###Vers le min de Fvalue:
    while PosF not in CloseList and PosI != PosF:
        
        if np.all(np.isnan(Fvalue)): #Check si F est égale à une matrice Full NaN
#            print('Pas de chemin')
            return(False) # soit return False, soit return la position init, donc bon..
        
        Index = np.argwhere(Fvalue == np.nanmin(Fvalue))
        PosI = Index.tolist()[0]
        
        CloseList.append(tuple(PosI))
        if PosI[0]-1>=0 and Map[PosI[0]-1,PosI[1]] != 1 and ((PosI[0]-1,PosI[1]) not in OpenList) and ((PosI[0]-1,PosI[1]) not in CloseList):  #Check vertical haut
            OpenList.append(((PosI[0]-1,PosI[1]),'D'))      #DOWN (fleche vers le bas..)
        if PosI[0]+1<=np.shape(Map)[0]-1 and Map[PosI[0]+1,PosI[1]] != 1 and ((PosI[0]+1,PosI[1]) not in OpenList) and ((PosI[0]+1,PosI[1]) not in CloseList): #Check vertical bas
            OpenList.append(((PosI[0]+1,PosI[1]),'U'))      #Up
        if PosI[1]-1>=0 and Map[PosI[0],PosI[1]-1] != 1 and ((PosI[0],PosI[1]-1) not in OpenList) and ((PosI[0],PosI[1]-1) not in CloseList): #Check horiz gauche
            OpenList.append(((PosI[0],PosI[1]-1),'R'))      #Right
        if PosI[1]+1<=np.shape(Map)[1]-1 and Map[PosI[0],PosI[1]+1] != 1 and ((PosI[0],PosI[1]+1) not in OpenList) and ((PosI[0],PosI[1]+1) not in CloseList): #Check horiz droit
            OpenList.append(((PosI[0],PosI[1]+1),'L'))      #Left
            
        for OV in OpenList:
            Gvalue[OV[0][0],OV[0][1]] = 10
                    
        Fvalue = np.copy(Gvalue + Hvalue)
        for CV in CloseList:
            Fvalue[CV[0],CV[1]] = np.nan
        

                       
############## TRACING BACK 
    PosF = InitialPosF

    while InitialPosI not in Chemin:
        
        for Trace in OpenList:
            if Trace[0] == PosF:
                Chemin.append(PosF)
                if Trace[1] == 'U':
                    PosF = (PosF[0]-1,PosF[1]) #Go up
                elif Trace[1] == 'D':
                    PosF = (PosF[0]+1,PosF[1]) #Go down
                elif Trace[1] == 'L':
                    PosF = (PosF[0],PosF[1]-1) #Go left
                elif Trace[1] == 'R':
                    PosF = (PosF[0],PosF[1]+1) #Go right
#                else:
#                    print(Chemin)
    Chemin.reverse()
    return(Chemin)
        
    

# Test
if __name__=='__main__':
    Map = np.zeros((5,5))
    Map[1,3] = 1
    Map[2,4] = 1
    Map[3,2] = 1
    Map[3,1] = 1
    Map[4,2] = 0
#    Map[4,0] = 1
#    Map[4,3] = 1
    
    Map[2,2] = 0
    Map[1,2] = 1
    Map[0,2] = 0

    PosI = (0,4)
    PosF = (4,1)
    
    Map[PosI[0],PosI[1]] = 88
    Map[PosF[0],PosF[1]] = 99
    
    Chemin = find(Map, PosI, PosF)
    print('le chemin est:', Chemin)    
    
    for C in Chemin[1:len(Chemin)-1]: #Test préliminaire 1
        Map[C[0],C[1]] = 5
        
    print(Map)
