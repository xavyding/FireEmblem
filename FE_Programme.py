# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:36:14 2017

@author: yixin.ding
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:08:53 2017

@author: Vignesh
"""

import numpy as np
import FE_Pathfinding as Path
import FE_Distancefinding as Df
import random
import pandas as pd


#Classe gérant l'environnement des Unités des Joueurs : elle permet l'initialisation  
#des caractéristiques d'une carte (taille de la carte, présence d'unités sur la carte, type de case, obstacles).
#Elle se met à jour régulièrement pour la présence des unités et une fois en début de jeu pour la définition du terrain
class Map:
    def __init__(self):
       
        self.terrain=np.zeros((10,15),int) #matrice contenant les etats du terrain
        self.PositionsPersos=np.zeros((10,15),tuple) #Matrice contenant les occupations des unités de chaque Joueur sur la Carte
        self.Terrains={0:"plaine", 1:"foret" , 2:"montagne", -1:"mur"} #types de terrain possibles
        self.plaine=0
        self.montagne=2
        self.foret=1
        self.mur=-1;
        self.l=self.PositionsPersos.shape
        self.Obstacle = np.zeros((10,15),int) #Obstacle, matrice contenant les cases interdites au déplacement:
        self.NumberMap = 1

    def Maj(self,liste_de_joueurs): 
        #liste_de_joueurs :  liste contenant les 2  classes Joueur qui jouent sur le jeu.
        # actualisation de la carte pour les positions des unités et leur présence (mort ou non)
        for i in range(0,self.l[0]):
                    for f in range(0,self.l[1]) :

                        self.PositionsPersos[i,f]=0
                        
        for J in liste_de_joueurs:
            for k in J.unites:
                self.PositionsPersos[k.position[0],k.position[1]]=(k.marqueur,k.Appartenance) #affiche aussi à qui appartient l'unité (J)
        
        
        self.Obstacle = np.zeros((10,15),int)
        for i in range(np.shape(self.terrain)[0]):
            for j in range(np.shape(self.terrain)[1]):
                if self.terrain[i,j] == -1 or self.PositionsPersos[i,j] !=0:
                    self.Obstacle[i,j] = 1
                     
    def SetMap(self): #creation d'un terrain contenant des etats de terrain
        if self.NumberMap == 1:
            self.terrain = pd.read_excel("Texture/Map/6/DATAMAP6.xlsx")
            self.terrain = self.terrain.as_matrix()

        elif self.NumberMap == 2:
            self.terrain = pd.read_excel("Texture/Map/8/DATAMAP8.xlsx")
            self.terrain = self.terrain.as_matrix()
            
        for i in range(np.shape(self.terrain)[0]):
            for j in range(np.shape(self.terrain)[1]):
                if self.terrain[i,j] == -1:
                    self.Obstacle[i,j] = 1

        
#Classe définissant les caractéristiques du Joueur: il possède une armée, 
#un nom et joue sur une Carte
class Joueur:
    def __init__(self,Carte,nom):
        #Carte : objet de classe Map
        #nom : objet de type 'string' désignant le Joueur
        self.nom=nom
        self.Carte=Carte
        self.UnitesDispo={1:'General1',2:'General2',3:'Eliwood1',4:'Eliwood2'}
        self.PV={'General1':15,'General2':15,'Eliwood1':8,'Eliwood2':8}
        self.unites=[]
        self.l=len(self.unites)
        self.tourfini = False   # doit devenir True si Joueur a fini toute les actions qu'il veut dans le tour actuel

    def __repr__(self):
        return 'Joueur Humain appelé {}'.format(self.nom)

            
    def assigner_unites(self,cle,pos0):
        #cle : objet de typoe int compris entre 1 et 4 inclu permettant de selectionner 
        #      une unité parmi celles proposées dans UnitesDispo
        #pos0 : objet de type liste de taille (1,2) contenant la position initiale de l'unité
        self.unites+=[Unité(self.UnitesDispo[cle],pos0,cle,self.PV[self.UnitesDispo[cle]],self.nom)]
        self.l=len(self.unites)
    def MajArmee(self):
        ind_elimine=-1
        for k in self.unites:
            if k.PV<=0:
                for i in range(0,len(self.unites)):
                    if k.nom==self.unites[i].nom:
                        ind_elimine=i
            if ind_elimine>=0:
                del self.unites[ind_elimine]
                self.l=self.l-1
                ind_elimine=-1


#Classe Joueur avec une IA intelligente. Ses choix d'actions (déplacements, combats) 
#sont basés sur des critères : chaque action potentielle augmente un score d'action par case (u.critere_map)
# dans la zone de déplacement possible de chaque unité. Ce score est calculé selon la présence d'unité ennemies 
#ou alliées proche de la case et de leurs PV, selon le type de terrain de la case. La décision d'action est alors prise 
#pour la case ayant le score maximale. En cas d'égalité de score entre deux cases, la première à avoir été calculée est choisie 
class JoueurIA(Joueur):
    
    def __init__(self, carte , nom):
        super().__init__(carte, nom)
        #carte : objet de classe Map
        #nom : objet de type 'string' désignant le Joueur
        self.Carte = carte
        self.tourfini = False        
        self.MC = None # Meilleure case, utilisée uniquement si 
        #l'IA ne trouve pas de choix parmi ses cases déplaçables

    def __repr__(self):
        return 'Joueur Ordinoïde appelé {}'.format(self.nom)

#Initilisation de la matrice contenant le score de chaque case dans la Carte pour une Unité    
    def Init_Crit_map(self,u):
        #u : objet de type Unité
        
        u.crit_map = np.ones(np.shape(self.Carte.terrain))
        L=np.shape(u.crit_map)
        
        
#        if self.Carte.terrain[int(L[0]/2),int(L[1]/2)] != -1:  #???????
#            u.crit_map[int(L[0]/2),int(L[1]/2)] = 10
#        if self.Carte.terrain[int(L[0]/2)-1,int(L[1]/2) ] != -1:
#            u.crit_map[int(L[0]/2)-1,int(L[1]/2)] = 10
#        if self.Carte.terrain[int(L[0]/2),int(L[1]/2)+1] != -1:
#            u.crit_map[int(L[0]/2),int(L[1]/2)+1] = 10
#        if self.Carte.terrain[int(L[0]/2)+1,int(L[1]/2) ] != -1:
#            u.crit_map[int(L[0]/2)+1,int(L[1]/2)] = 10
        
        #Eliminer les zones impossibles
        for i in range(L[0]):
            for j in range(L[1]):
                if abs(i-u.position[0])+abs(j-u.position[1]) > u.vitesse:
                    u.crit_map[i,j] = -float(np.inf)

    def Choix_unite_IA(self,liste_unites_totale):
#       liste_unites_totale : objet de type liste contenant tous les objets de type 
        #                     Unité utilisés par les deux Joueurs
        Unites_jouables = []
        dist = 2000
        for u in self.unites:
            if u.pasencoredéplacée == True or u.pasencorecombattu == True:
                Unites_jouables.append(u)
                
        
        if Unites_jouables == []:
            self.tourfini = True
            return False
        else:
            for u in Unites_jouables :
                MAP = u.CaseDeplacable_calcul(self.Carte)
                self.Init_Crit_map(u)  
                for i in range(0,np.shape(MAP)[0]) :
                    for j in range(0,np.shape(MAP)[1]) :
                        if MAP[i,j] != False and abs(i-u.position[0])+abs(j-u.position[1]) <= u.vitesse:
                            self.Critere(u,(i,j),MAP,liste_unites_totale)
    
            M = - float(np.inf) 
            unite_a_jouer = None
            
            for u in Unites_jouables :    
                if np.max(u.crit_map) > M : 
                    M = np.max(u.crit_map)
                    unite_a_jouer = u


#       Cas où l'IA ne trouve pas de case jouer car path.find à coté des unités ennemies renvoie False (car trop loin)     
            if M <= 60 : 
                print("no decision within reach")
                
                self.WR = False
                
                UA = [] #Liste contenant les autres unités alliées
                UE = [] #Liste contenant les autres unités ennemies
     
                for unit in Unites_jouables:
                    if unit.Appartenance == u.Appartenance:
                        UA.append(unit)
                    
                for unit in liste_unites_totale:
                    if unit.Appartenance != u.Appartenance:
                            UE.append(unit)
                        
                for u in UA :
                    MAP = u.CaseDeplacable_calcul(self.Carte)
                    for e in UE:
                        for i in range(0,np.shape(MAP)[0]) :
                            for j in range(0,np.shape(MAP)[1]):
                                if MAP[i,j] != False :
                                    if dist >= abs(i - e.position[0]) + abs(j - e.position[1]):
                                        dist = abs(i - e.position[0]) + abs(j - e.position[1])
                                        self.MC =[i,j]
                                        unite_a_jouer = u                                       
            else:
                self.WR = True
                
            if self.MC == None :
                M = - float(np.inf) 
                unite_a_jouer = None
            
                for u in Unites_jouables :    
                    if np.max(u.crit_map) > M : 
                        M = np.max(u.crit_map)
                        unite_a_jouer = u
                self.WR = True
                
            if len(Unites_jouables) <= 1:
                self.tourfini = True
                
            return unite_a_jouer
    
    
    def deplacement_IA(self,u): # + en entrée liste TOUT LES UNITES
        
        #u : objet de type Unité
        if u != False and u.pasencoredéplacée == True and self.WR == True:
            PositionF = np.argwhere(u.crit_map == np.max(u.crit_map))[0]
            chemin = Path.find(self.Carte.Obstacle, (u.position[0],u.position[1]),(PositionF[0],PositionF[1]))

            u.pasencoredéplacée = False
            return chemin[1:]
        
        elif u != False and u.pasencoredéplacée == True and self.WR == False :
            
            PositionF = np.argwhere(u.crit_map == np.max(u.crit_map))[0]
            PositionF[0],PositionF[1] = self.MC[0], self.MC[1]
            chemin = Path.find(self.Carte.Obstacle, (u.position[0],u.position[1]),(PositionF[0],PositionF[1]))
            u.pasencoredéplacée = False
            return chemin[1:]
                       
        else:
            return(False)
    
    def combat_IA(self,u,liste_unites_totale):
        #u : objet de type Unité
#       liste_unites_totale : objet de type liste contenant tous les objets de type 
        #                     Unité utilisés par les deux Joueurs
        focus = None
        focus_list = []
        if u != False and u.pasencorecombattu == True:
            dist = 0
            UA = [] #Liste contenant les autres unités alliées
            UE = [] #Liste contenant les autres unités ennemies
     
            for unit in liste_unites_totale:
                if unit.Appartenance == u.Appartenance:
                    UA.append(unit)
                else:
                    UE.append(unit)
            for e in UE:          #e est une unité enemie      
                dist = abs(u.position[0] - e.position[0]) + abs(u.position[1] - e.position[1])
                if dist <= 1:
                    focus_list.append(e)
                    
            PV = float(np.inf)
            for enemie in focus_list: #Choisir l'enemie qui a le moins de PV
                if enemie.PV < PV:
                    PV = enemie.PV
                    focus = enemie
                    
            if focus == None:
                u.pasencorecombattu = False
                return(False)
            else:
                if u.type=='Atq':
                    focus.PV= focus.PV-(u.degat+self.Carte.terrain[u.position[0],u.position[1]])
                u.pasencorecombattu = False
                return(focus)                                       
        else:
            return(False)



    def Critere(self,u, c, MAP, liste_unites_totale): 
        
#       u: objet de type unité, unité que l'on cherche à jouer 
#       c: objet de type tuple, contient coordonnées vers lesquelles on veut se déplacer, 
#       MAP: Obstacle objet de type array, provenant de la classe Map (voir définition de la classe)   
#       liste_unites_totale : objet de type liste contenant tous les objets de type 
#                             Unité utilisés par les deux Joueurs

        UA = [] #Liste contenant les autres unités alliées
        UE = [] #Liste contenant les autres unités ennemies
        for unit in liste_unites_totale:
            if unit.Appartenance == u.Appartenance :
                UA.append(unit)
            else:
                UE.append(unit)
       
        if MAP[c[0],c[1]] != False :
 
            if Path.find(self.Carte.Obstacle, tuple(u.position) , c ) != False :
                u.crit_map[c[0],c[1]] += 10
                        
                for e in UE :
                            
                    if e.position[0]+1 == c[0] and e.position[1] == c[1]:
                        u.crit_map[c[0],c[1]] += 50
                        if e.PV < u.PV:
                            u.crit_map[c[0],c[1]] += 50
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='foret':
                            u.crit_map[c[0],c[1]] += 10
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='montagne':
                            u.crit_map[c[0],c[1]] += 20
                                
                    if e.position[0]-1 == c[0] and e.position[1] == c[1]:
                        u.crit_map[c[0],c[1]] += 50
                        if e.PV < u.PV:
                            u.crit_map[c[0],c[1]] += 50
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='foret':
                            u.crit_map[c[0],c[1]] += 10
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='montagne':
                            u.crit_map[c[0],c[1]] += 20
                                
                    if e.position[0] == c[0] and e.position[1]+1 == c[1]:
                        u.crit_map[c[0],c[1]] += 50
                        if e.PV < u.PV:
                            u.crit_map[c[0],c[1]] += 50
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='foret':
                            u.crit_map[c[0],c[1]] += 10
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='montagne':
                            u.crit_map[c[0],c[1]] += 20
                                
                    if e.position[0]+1 == c[0] and e.position[1]-1 == c[1]:
                        u.crit_map[c[0],c[1]] += 50
                        if e.PV < u.PV:
                            u.crit_map[c[0],c[1]] += 50
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='foret':
                            u.crit_map[c[0],c[1]] += 10
                        if self.Carte.Terrains[self.Carte.terrain[c[0],c[1]]] =='montagne':
                            u.crit_map[c[0],c[1]] += 20 
                
            if Path.find(self.Carte.Obstacle, tuple(u.position) , (c[0]+1, c[1] )) != False:
                 u.crit_map[c[0],c[1]] += 10  
                         
            if Path.find(self.Carte.Obstacle, tuple(u.position) , (c[0]-1, c[1] )) != False:
                u.crit_map[c[0],c[1]] += 10
                    
            if Path.find(self.Carte.Obstacle, tuple(u.position) , (c[0], c[1]+1)) != False:
                u.crit_map[c[0],c[1]] += 10
                    
            if Path.find(self.Carte.Obstacle, tuple(u.position) , (c[0], c[1]-1 )) != False:
                u.crit_map[c[0],c[1]] += 10
                
#         for a in UA : 
#            MAPS = a.CaseDeplacable_calcul(self.Carte)
#            if c[0]+1 < 15 :
#                if MAPS[c[0]+1,c[1]] != False :
#                    u.crit_map[c[0],c[1]] += 10
#            if c[0]-1 > 0:    
#                if MAPS[c[0]-1,c[1]] != False :
#                    u.crit_map[c[0],c[1]] += 10
#            if c[1]+1 < 15:
#                if MAPS[c[0],c[1]+1] != False :
#                    u.crit_map[c[0],c[1]] += 10
#            if c[1]-1 > 0:
#                if MAPS[c[0],c[1]-1] != False :
#                    u.crit_map[c[0],c[1]] += 10               
            
                    
#Classe Joueur Ordinateur dont l'intelligence est "aléatoire" i.e ses choix de déplacement 
# et d'attaque sont aléatoires
class Joueur_Random(Joueur):
    
    def __init__(self, carte , nom):
        super().__init__(carte, nom)
        
        
    def __repr__(self):
        return 'Joueur Random appelé {}'.format(self.nom)
    
              
    def Choix_unite_IA_Random(self):
        Unites_jouables = []
        for u in self.unites:
            if u.pasencoredéplacée == True or u.pasencorecombattu == True:
                Unites_jouables.append(u)
                
        if Unites_jouables == []:
            self.tourfini = True
            return False
        else:
            unite_a_jouer = random.choice(Unites_jouables)                              
            if len(Unites_jouables) <= 1:
                self.tourfini = True
            return unite_a_jouer
    
    
    def deplacement_IA_Random(self,u):
        MAP = u.CaseDeplacable_calcul(self.Carte)
        PositionOK = []
        for i in range(np.shape(MAP)[0]):
            for j in range(np.shape(MAP)[1]):
                if MAP[i,j]:
                    PositionOK.append((i,j))
        if PositionOK != [] and u.pasencoredéplacée == True:
            u.pasencoredéplacée = False
            chemin = Path.find(self.Carte.Obstacle, (u.position[0],u.position[1]),random.choice(PositionOK))
            return(chemin[1:])
        else:
            return False
            
    
    def combat_IA_Random(self,u,liste_unites_totale):
        focus = None
        focus_list = []
        if u != False and u.pasencorecombattu == True:
            dist = 0
            UA = [] #Liste contenant les autres unités alliées
            UE = [] #Liste contenant les autres unités ennemies
     
            for unit in liste_unites_totale:
                if unit.Appartenance == u.Appartenance:
                    UA.append(unit)
                else:
                    UE.append(unit)
            for e in UE:          #e est une unité enemie      
                dist = abs(u.position[0] - e.position[0]) + abs(u.position[1] - e.position[1])
                if dist <= 1:
                    focus_list.append(e)
                    
            if focus_list:
                focus = random.choice(focus_list)
                
            if focus == None:
                u.pasencorecombattu = False
                return(False)
            else:
                if u.type=='Atq':
                    focus.PV= focus.PV-(u.degat++self.Carte.terrain[u.position[0],u.position[1]])
                u.pasencorecombattu = False
                return(focus)                                       
        else:
            return(False)

        


#Classe définissant toutes les caractéristiques(PV,position,vitesse,dégât,rôle,appartenance au joueur)
# de l'Unité ainsi que sa jouabilité (déjà combattu, déjà déplacée, meilleure choix de jeu pour l'IA et déplaçabilité)
class Unité: # contient l'ensemble des carac d'une unité
    def __init__(self,nom,pos0,marqueur,PV,Appartenance):
#       nom : objet de type 'string', désignation de l'unité
#       pos0 : objet de type 'list' de taille (1,2) contenant la position de départ
#       marqueur : objet de type _______ permettant de dsitinguer les unités entre elles, y compris celles de nom identique
#       PV : objet de type 'int', représente le nombre de PV de l'unité
#       Appartenance : objet de type 'string' contient le nom du Joueur possédant l'unité
        self.pasencoredéplacée=True
        self.pasencorecombattu=True        
        self.CaseDeplacable = None        
        self.crit_map = None
        self.nom=nom
        self.Appartenance = Appartenance # Appartenance à un joueur, servi dans la partie combat
        self.PV=PV
        self.PVmax=PV
        self.role={1:'Atq',2:'Soin'} #permet de savoir si l'unité permet d'attaquer OU de soigner (un seulement)
        self.position=pos0
        self.marqueur=marqueur #permet de savoir quelle unité c'est sur la Map
        self.vitesse=1 # permet de déterminer ensuite le déplacement maximal de l'unité
        if self.nom =='General1':
            self.vitesse=5
            self.degat = 1
            self.type=self.role[1]
        elif self.nom=='General2':
            self.vitesse=5
            self.degat = 1
            self.type=self.role[1]
        elif self.nom=='Eliwood1':
            self.vitesse=6
            self.degat = 3
            self.type=self.role[1]
        elif self.nom=='Eliwood2':
            self.vitesse=6
            self.degat = 3
            self.type=self.role[1]
            
    def CaseDeplacable_calcul(self,Carte):
#       Carte : objet de type Map
        Carte = Carte
        MapObstacle = Carte.Obstacle
        
        if self.pasencoredéplacée:            
            if Carte.Terrains[Carte.terrain[self.position[0],self.position[1]]] == 'montagne':
                if self.nom.startswith('G'):
                    self.vitesse = 3
                elif self.nom.startswith('E'):
                    self.vitesse = 4
            elif Carte.Terrains[Carte.terrain[self.position[0],self.position[1]]] == 'foret':
                if self.nom.startswith('G'):
                    self.vitesse = 4
                elif self.nom.startswith('E'):
                    self.vitesse = 5
            elif Carte.Terrains[Carte.terrain[self.position[0],self.position[1]]] == 'plaine':
                if self.nom.startswith('G'):
                    self.vitesse = 5
                elif self.nom.startswith('E'):
                    self.vitesse = 6
            DM = Df.Distancemap(MapObstacle,(self.position[0],self.position[1]),self.vitesse)
            return(DM<=self.vitesse)
        else:
            return((MapObstacle<-np.inf))
            
    def __repr__(self):
        return 'Unité {}'.format(self.nom)
    


            
#Classe qui permet les actions de joueurs qui sont : deplacement d'une unité 
#et attaque par une unité d'une unité ennemie.
#On remarquera deux fonctions similaires pour chaque action : deplacement, deplacement_return   
#et combat,combat_return. La fonction sans le suffixe "_return" est utilisé par le programme en console
# celle avec le suffixe"_return" est utilisée pour l'interface graphique pour diverses contraintes.
class Coup:
    
    def __init__(self,unité,Carte):
#       unité : objet de type Unite
#       Carte : objet de type Map
        self.Unit=unité  #prend en entrée un objet de classe unité
        self.Carte = Carte #prend en entrée un objet de classe carte
        self.Chemin = []
    
    def deplacement(self,h,v):
#        h,v : objets de type 'int', ils représentent les coordonnées dans la matrice
        deplacementestautorisé = False
        # ajouter une ligne pour modifier la vitesse suivant l'état de terrain (?? ici ou dans classe unité??)
        if h<=np.shape(self.Carte.terrain)[0] and v<=np.shape(self.Carte.terrain)[1] and h>=0 and v>=0:
            if abs(self.Unit.position[0]-h)+abs(self.Unit.position[1]-v)<=self.Unit.vitesse: #si leur capacité de déplacement leur permet
                if (self.Carte.terrain[h,v] !=-1) and (self.Carte.PositionsPersos[h,v]==0):
                    if self.Unit.pasencoredéplacée == True:
                        deplacementestautorisé = True
                    else:
                        deplacementestautorisé = False
                else:
                    deplacementestautorisé = False
            else:
                deplacementestautorisé = False                   
        else:
            deplacementestautorisé = False
        
        if deplacementestautorisé:
            self.Chemin = Path.find(self.Carte.Obstacle, (self.Unit.position[0],self.Unit.position[1]),(h,v))
            self.Unit.position = [h,v]
            self.Unit.pasencoredéplacée = False
            
#            print('le chemin est',self.Chemin)
            
        else:
            print('le déplacement est impossible')
            
    def deplacement_return(self,h,v):
#        h,v : objets de type 'int', ils représentent les coordonnées dans la matrice
        deplacementestautorisé = False
        # ajouter une ligne pour modifier la vitesse suivant l'état de terrain (?? ici ou dans classe unité??)
        if h<=np.shape(self.Carte.terrain)[0] and v<=np.shape(self.Carte.terrain)[1] and h>=0 and v>=0:            
            if (self.Carte.terrain[h,v] !=-1) and (self.Carte.PositionsPersos[h,v]==0):
                if Path.find(self.Carte.Obstacle, (self.Unit.position[0],self.Unit.position[1]),(h,v)) != False: #s'il existe un chemin
                    if len(Path.find(self.Carte.Obstacle, (self.Unit.position[0],self.Unit.position[1]),(h,v)))-1 <= self.Unit.vitesse: #si leur capacité de déplacement leur permet
                        if self.Unit.pasencoredéplacée == True:
                            deplacementestautorisé = True
                        else:
                            deplacementestautorisé = False
                    else:
                        deplacementestautorisé = False
                else:
                    deplacementestautorisé = False
            else:
                deplacementestautorisé = False                   
        else:
            deplacementestautorisé = False
        
        if deplacementestautorisé:
            self.Unit.pasencoredéplacée = False
            self.Chemin = Path.find(self.Carte.Obstacle, (self.Unit.position[0],self.Unit.position[1]),(h,v))
            return(self.Chemin[1:])            
        else:
            print('le déplacement est impossible')
            return([(self.Unit.position[0],self.Unit.position[1])])            
            
            
            
    def combat(self,UniteD): 
#       UniteD : objet de classe Unite, il représente l'unité attaquée par 
#               l'unité utilisée dans l'initialisation de la classe Coup
        distance=abs((self.Unit.position[0]-UniteD.position[0])+(self.Unit.position[1]-UniteD.position[1]))       
        if distance == 1 and self.Unit.pasencorecombattu==True:
            if self.Unit.type=='Atq' and self.Unit.Appartenance != UniteD.Appartenance:
                UniteD.PV=UniteD.PV-self.Unit.degat
                self.Unit.pasencorecombattu=False                
#                if UniteD.PV>0:
#                    self.Unit.PV=self.Unit.PV-UniteD.degat
#                    self.Unit.pasencorecombattu=False
#                    
#            elif self.Unit.type=='Soin' and self.Unit.Appartenance == UniteD.Appartenance and UniteD.PV<UniteD.PVmax:
#                    UniteD.PV+=1
#                    self.Unit.pasencorecombattu=False
            else:
                print("action impossible, il s'agit d'une unité alliée ")
                
 
        else:
            print("Action impossible l'unité visée est incorrecte (trop loin ou il s'agit d'elle même ou déja combattu dans ce tour")
              
    def passer(self):
        self.Unit.pasencoredéplacée = False
        self.Unit.pasencorecombattu = False
        
    def combat_return(self,UniteD):
#       UniteD : objet de classe Unite, il représente l'unité attaquée par 
#               l'unité utilisée dans l'initialisation de la classe Coup
        
        distance = np.square(self.Unit.position[0]-UniteD.position[0]) + np.square(self.Unit.position[1]-UniteD.position[1])

        if distance == 1 and self.Unit.pasencorecombattu==True:
            if self.Unit.type=='Atq' and self.Unit.Appartenance != UniteD.Appartenance:
                UniteD.PV=UniteD.PV - (self.Unit.degat + self.Carte.terrain[self.Unit.position[0],self.Unit.position[1]])    
                self.Unit.pasencorecombattu=False               
                return([UniteD.position[0],UniteD.position[1]])
                
#----------------------------------------------------------------------------------------------------------------------------------------                
# Non prise en compte des répliques et de la capacité de soin               
#                if UniteD.PV>0:
#                    self.Unit.PV=self.Unit.PV-UniteD.degat
#                    self.Unit.pasencorecombattu=False
#                    
#            elif self.Unit.type=='Soin' and self.Unit.Appartenance == UniteD.Appartenance and UniteD.PV<UniteD.PVmax:
#                    UniteD.PV+=1
#                    self.Unit.pasencorecombattu=False
#                    return([[UniteD.position[0],UniteD.position[1]]])
#------------------------------------------------------------------------------------------------------------------------------------------
            else:
                print("action impossible, il s'agit d'une unité alliée ")
                return None
 
        else:
            print("Action impossible l'unité visée est incorrecte (trop loin ou il s'agit d'elle même ou déja combattu dans ce tour")
            return None
            
        
              
  
# Classe permettant jeu tour par tour, et définissant le Vainqueur du Jeu 
#(si un Joueur n'a plus d'unités, il a perdu).       

class Tour:
    def __init__(self):
        self.victoire = 0
        self.de = None
        self.Jeufini = False  
    def nouveautour(self,joueur1,joueur2):
#       joueur1,joueur2 : objets de type 'Joueur', représentant les deux Joueurs du jeu
        joueur1.tourfini = False
        joueur2.tourfini = False
        for i in joueur1.unites:
            i.pasencoredéplacée = True
            i.pasencorecombattu = True
        for i in joueur2.unites:
            i.pasencoredéplacée = True
            i.pasencorecombattu = True
    
    def victoire(self,joueur1,joueur2):
        if joueur1.unites == [] and joueur2.unites == []:
            print('Commencer la partie')
            return(False)
            
        if joueur1.unites == []:
            print("Victoire de :",self.Joueur2.nom)
            self.Jeufini = True
            return self.Joueur2.nom
        elif joueur2.unites == []:
            print("Victoire de :",self.Joueur1.nom)
            self.Jeufini = True
            return self.Joueur1.nom
            
        else :
            print("la partie continue")
            return False
            
#il s'agit de la fonction permettant de selectionner une unité. 
#Sa définition est neutre, cependant la fonction sélectionner dépend du Joueur qui l'utilise
class Curseur: 

    def __init__(self,Carte):
#       Carte : objet de type Map
        self.position=[0,0]
        self.carte = Carte
        self.typeterrain=Carte.terrain
        self.occupation = Carte.PositionsPersos

        
    def deplacer_curseur(self,h,v):
#        h,v : objets de type 'int', ils représentent les coordonnées dans la matrice
        if h<=np.shape(self.typeterrain)[0] and v<=np.shape(self.typeterrain)[1] and h>=0 and v>=0:
            self.position=[h,v]
        else:
            print('Déplacement impossible')
            None
       
    def selectionner(self,Joueur):
#        Joueur: objet de type 'Joueur', représentant le Joueur sélectionnant une de ses unités
        if self.occupation[self.position[0],self.position[1]] !=0:
            if self.occupation[self.position[0],self.position[1]][1] == Joueur.nom:
                for k in Joueur.unites:
                    if k.position == [self.position[0],self.position[1]]:

                        return k
                else:
                    print("UNE ERREUR S'EST PRODUITE, REDEMARREZ VOTRE ORDINATEUR, CODE:TR011 :(")
            else:
                print('Sélection Impossible: cette unité ne vous apparetient pas')
                return(False)
        else:
            print("Il n'y a rien ici")
            return(False)
            
    def info(self):
        nomtypeterrain = {0:"plaine",1:"montagne",2:"foret",-1:"mur"}
        print("Position: {},{}  -  Terrain: {}  -  Occupation: {}".format(self.position[0],self.position[1],nomtypeterrain[self.typeterrain[self.position[0],self.position[1]]],self.occupation[self.position[0],self.position[1]]))
        return(None)
              





#classe permettant le déplacement d'un objet dans un plan cartésien 
#(utilisé au final uniquement pour WallItem)
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate_inplace(self, vec):
        dx, dy = vec
        self.x += dx
        self.y += dy

    def translate_outofplace(self, vec):
        p = Position(self.x, self.y)
        p.translate_inplace(vec)
        return p

    def distance(self, pos):
        return (pos.x - self.x) ** 2 + (pos.y - self.y) ** 2

    def __eq__(self, pos):
        if pos.x == self.x and pos.y == self.y:
            return True
        return False

#classe parente pour le type d'objet et sa position, 
class Artefact:
    def __init__(self):
        self.type = None
        self.pos = Position(0, 0)

# je creer une classes qui va contenir toutes mes cases de façon générale voir
#WallManager
class WallItem(Artefact):
    def __init__(self, x, y):
        self.type = 'wall'
        self.pos = Position(x, y)    
    
#Cette classe rempli une liste vide, avec des cases vides pour définir une fenêtre 
#affichant la partie graphique du jeu (carte,persos).
class WallManager():
    def __init__(self, w, h):
#        w,h : objets de type 'int'
        self.w = w #definition du nombre de cases dans la fenêtre
        self.h = h
        self.walls = []
        self.create_border()

    def create_border(self):
        
        for i in range(self.h):
            self.walls+= [WallItem(col, i) for col in range(self.w)]

    def load_map(self, filename):
        self.walls = []
        pass

    def get_walls(self):
        return self.walls




#fonction mettant en place les classes Joueurs, la classe Carte sur laquelle évolue le jeu, 
#les classe Unités de chaque Joueur et enfin la classe Tour permettant de le jeu tour par tour

def testInitialisation():
    Carte=Map()
    Yixin=Joueur(Carte,'Yixin')
    Yixin.assigner_unites(1,[0,0])
    Yixin.assigner_unites(2,[0,1])
    Vignesh=Joueur(Carte,'Vignesh')
    Vignesh.assigner_unites(3,[4,4])

    
    print('Terrain\n',Carte.terrain)
    Carte.SetMap()
    print('Terrain\n',Carte.terrain)
    
    Carte.Maj([Yixin,Vignesh])
    print('Carte Positions des persos\n',Carte.PositionsPersos)
    
    print('Obstacles: \n',Carte.Obstacle)
    
    T=Tour()



# On regarde si le Joueur arrive à commander via la classe Coup le déplacement d'une unité à la position voulue,
#tout en respectant les régles du jeu (cases inaccessibles pour diverses raisons comme : 
#case déjà occupée, case trop loin pour être atteinte par l'unité)
#IMPLEMENTER LE PATH FIND ???? de plus ce n'est pas un tour chacun normalement ? là on est avec un tour pour les deux
def testDeplacement1():
    
#-------------------------------------------------Bloc testé par testInitialisation-----------------------------------------------------    
    Carte=Map()
    Yixin=Joueur(Carte,'Yixin')
    Yixin.assigner_unites(1,[0,0])
    Yixin.assigner_unites(2,[0,1])
    Vignesh=Joueur(Carte,'Vignesh')
    Vignesh.assigner_unites(3,[4,4])
    Carte.SetMap()   
    Carte.Maj([Yixin,Vignesh])


#----------------------------------------------------------------------------------------------------------------------------------------  
   
    T=Tour()

    Coup(Yixin.unites[0],Carte).deplacement(1,3)
    print('Position unite Roy de {name}'.format(name=Yixin.nom),Yixin.unites[0].position)    
    Coup(Vignesh.unites[0],Carte).deplacement(1,3)
    print('Position unite Lyn de {name}'.format(name=Vignesh.nom),Vignesh.unites[0].position)
    
    
    T.nouveautour(Yixin, Vignesh)

  
    Coup(Yixin.unites[0],Carte).deplacement(2,3)
    print('Position unite Roy de {name}'.format(name=Yixin.nom),Yixin.unites[0].position) 
    Carte.Maj([Yixin,Vignesh])
    print('Carte Positions des persos\n',Carte.PositionsPersos)
    
 
    
# On teste ici le bon fonctionnement du curseur : permet la selection d'unités 
#et leur déplacement là où le curseur se trouve. De plus une unité ne poeut plus 
#être déplacée après un déplacement 
def testDeplacement2(): 
    
#-------------------------------------------------Bloc testé par testInitialisation-----------------------------------------------------    
    Carte=Map()
    Yixin=Joueur(Carte,'Yixin')
    Yixin.assigner_unites(1,[0,0])
    Yixin.assigner_unites(2,[0,1])
    Vignesh=Joueur(Carte,'Vignesh')
    Vignesh.assigner_unites(3,[4,4])
    Carte.SetMap()   
    Carte.Maj([Yixin,Vignesh])


#-------------------------------------------------Bloc testé par testDeplacement1---------------------------------------------------------------------------------------  
   
    T=Tour()

    Coup(Yixin.unites[0],Carte).deplacement(1,3)
    Coup(Vignesh.unites[0],Carte).deplacement(1,3)
    T.nouveautour(Yixin, Vignesh)
    Coup(Yixin.unites[0],Carte).deplacement(2,3)
    Carte.Maj([Yixin,Vignesh])

#--------------------------------------------------------------------------------------------------------------------------------------------    
    Cursor = Curseur(Carte)
    Cursor.deplacer_curseur(8,3)
    Cursor.info()
    
    Cursor.deplacer_curseur(2,3)
    Cursor.info()
    
# On teste ici si Vignesh peut sélectionner l'unité de Yixin (normalement non)
    Cursor.selectionner(Vignesh)
    Cursor.selectionner(Yixin)   
    T.nouveautour(Yixin, Vignesh)


# Il s'agit du tour d'Yixin, il déplace l'unité qu'il a selectionne en (2,3) (via la position curseur) à la position 1,3   
    Coup(Cursor.selectionner(Yixin),Carte).deplacement(1,3)
    Carte.Maj([Yixin,Vignesh])
    print(Yixin.unites[0].pasencoredéplacée)
    print('Carte Positions des persos\n',Carte.PositionsPersos)
    
# Déplace le curseur sur la deuxieme unité d'Yixin
    Cursor.deplacer_curseur(0,1)  
    

# Selectionner la deuxième unité de Yixin et la déplacer à (0,3)
    Coup(Cursor.selectionner(Yixin),Carte).deplacement(0,3) 
    Carte.Maj([Yixin,Vignesh]) #Mise à jour de la carte (/!\ Cette étape est OBLIGATOIRE)
    print('Carte Positions des persos\n',Carte.PositionsPersos) 
       
 
#Fonction permettant le test da fonction combat de la classe Coup. 
#Il faut que les unités perdent des PV, les dégâts des unités doivent changer 
#selon leur environnement et enfin les unités doivent disparaître si elles leurs PV tombent à zero
def testCombat():

#-------------------------------------------------Bloc testé par testInitialisation-----------------------------------------------------    
    Carte=Map()
    Yixin=Joueur(Carte,'Yixin')
    Yixin.assigner_unites(1,[0,0])
    Yixin.assigner_unites(2,[0,1])
    Vignesh=Joueur(Carte,'Vignesh')
    Vignesh.assigner_unites(3,[4,4])
    Carte.SetMap()   
    Carte.Maj([Yixin,Vignesh])


#-------------------------------------------------Bloc testé par testDeplacement1---------------------------------------------------------------------------------------  
   
    T=Tour()

    Coup(Yixin.unites[0],Carte).deplacement(1,3)
    Coup(Vignesh.unites[0],Carte).deplacement(1,3)
    T.nouveautour(Yixin, Vignesh)
    Coup(Yixin.unites[0],Carte).deplacement(2,3)
    Carte.Maj([Yixin,Vignesh])

#--------------------------------------------------Bloc testé par testDeplacement2------------------------------------------------------------    
    Cursor = Curseur(Carte)
    Cursor.deplacer_curseur(8,3)
    Cursor.info()   
    Cursor.deplacer_curseur(2,3)
    Cursor.info()    
    Cursor.selectionner(Vignesh)
    Cursor.selectionner(Yixin)   
    T.nouveautour(Yixin, Vignesh)   
    Coup(Cursor.selectionner(Yixin),Carte).deplacement(1,3)
    Carte.Maj([Yixin,Vignesh])      
    Cursor.deplacer_curseur(0,1)  
    Coup(Cursor.selectionner(Yixin),Carte).deplacement(0,2)
    Carte.Maj([Yixin,Vignesh])

#--------------------------------------------------------------------------------------------------------------------------------------------
    print("Degat de l'unite de Yixin",Yixin.unites[0].nom,Yixin.unites[0].degat)
    print("Degat de l'unite de Vignesh",Vignesh.unites[0].nom,Vignesh.unites[0].degat)
    
    print(Yixin.unites[0].Appartenance)
    

    Carte.Maj([Yixin,Vignesh]) #Mise à jour de la carte (/!\ Cette étape est OBLIGATOIRE)
    print('Carte Positions des persos',Carte.PositionsPersos) 
    

    print("PV de l'unite de Vignesh",Vignesh.unites[0].nom,Vignesh.unites[0].PV) 
    Coup(Yixin.unites[0],Carte).combat(Vignesh.unites[0])
    print("PV de l'unite de Vignesh",Vignesh.unites[0].nom,Vignesh.unites[0].PV)
    

# On vérifie que la deuxième unité de Yixin qui n'est pas au corps à corps avec 
#l'unité de Vignesh ne peut pas attaquer.
    Coup(Yixin.unites[1],Carte).combat(Vignesh.unites[0])
    print("PV de l'unite de Vignesh",Vignesh.unites[0].nom,Vignesh.unites[0].PV)
    
# On vérifie que la première unité de Yixin qui a déjà attaqué 
#l'unité de Vignesh ne peut pas attaquer une deuxième fois.    
    Coup(Yixin.unites[0],Carte).combat(Vignesh.unites[0])
    print("PV de l'unite de Vignesh",Vignesh.unites[0].nom,Vignesh.unites[0].PV)
    
# si une unité possède des PV<0 elle est retirée des unités jouables de Vignesh    
    Vignesh.MajArmee()
    
    
    T.nouveautour(Yixin, Vignesh) 
    
# On vérifie que les unités alliées d'un joueur ne peuvent pas s'attaquer entre elles
    Coup(Yixin.unites[1],Carte).deplacement(2,2)
    Coup(Yixin.unites[1],Carte).combat(Yixin.unites[0])
    print("PV de l'unite de Vignesh",Yixin.unites[0].nom,Yixin.unites[0].PV)
    
       
    print(Vignesh.unites)
    Carte.Maj([Yixin,Vignesh]) #Mise à jour de la carte (/!\ Cette étape est OBLIGATOIRE)
    print('Obstacles: \n',Carte.Obstacle)    
    print('Carte Positions des persos\n',Carte.PositionsPersos) 
   
if __name__=='__main__':
#    testInitialisation()
#    testDeplacement1()
#    testDeplacement2()
    testCombat()