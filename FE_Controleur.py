# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 11:41:46 2017

@author: Vignesh
"""

try:
    # Qt5
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtMultimedia import *
except ImportError:
    try:
        # Qt4
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
    except ImportError:
        print('Merci d\'installer PyQt5 ou PyQt4.')
        exit()

import random
import FE_Programme as PD






#Classe FEController: C'est le contrôleur du jeu, permettant de faire le lien entre le Programme et les parties Graphiques
class FEController:
    
    #Initialisation des variables
    def __init__(self):        
        self.w, self.h = 15, 10        
        self.NumberMap = 1
        
        self.carte = None
        self.WM = None 
        self.Tour = None
        self.Joueur1 = None
        self.Joueur2 = None
        self.curseur= None
        self.Tour_de = None
        self.Coup = None       
        self.liste_unites = []
        self.Personnages = []
        self.main_window = None
        self.view = None
        self.startparam = None
        self.startmessage = None
        self.startinfo = None
        self.Keyboard = False
        self.isFinished = False
        self.Victoire = False


        
    
        
# Création de la fenêtre du jeu        
    def set_main_window(self, window):
        self.main_window = window

# Création de VIEW (Partie Graphique du jeu)        
    def set_view(self, view):
        self.view = view

# Création de la carte (Classe Map du programme) 
    def getMap(self,carte):
        self.carte = carte
        return self.carte        

# Création de Tour (Classe Tour du programme)      
    def getTour(self):
        self.T= PD.Tour
        return self.T

# Création de Curseur (Classe Curseur du programme)            
    def getCursor(self):
        self.curseur = PD.Curseur(self.carte)
        return self.curseur
    
# Création du background pour la scene      
    def getWallManager(self,WallManager):
        self.WM = WallManager
        return self.WM

# Création des Joueurs (Classe Joueur du programme) 
    def set_players(self, nom_joueur1, nom_joueur2):
        #en entrée, les noms des joueurs (Classe str)
       
        if nom_joueur1.startswith('P') == True:
            self.Joueur1 = PD.Joueur(self.carte,nom_joueur1)
        elif nom_joueur1.startswith('B') == True:
            self.Joueur1 = PD.JoueurIA(self.carte,nom_joueur1)
        elif nom_joueur1.startswith('A') == True:
            self.Joueur1 = PD.Joueur_Random(self.carte,nom_joueur1)
        
        if nom_joueur2.startswith('P') == True:
            self.Joueur2 = PD.Joueur(self.carte,nom_joueur2)
        elif nom_joueur2.startswith('B') == True:
            self.Joueur2 = PD.JoueurIA(self.carte,nom_joueur2)
        elif nom_joueur2.startswith('A') == True:
            self.Joueur2 = PD.Joueur_Random(self.carte,nom_joueur2)
     
        return [self.Joueur1,self.Joueur2] 


# Création et affectation des unités aux joueurs.
    def getUnites(self):
        self.liste_unites =[]

        i = 1    #Set unites Player1     
        while i<=4:
            r = [random.randint(0,3),random.randint(0,3)] #Position d'apparition de l'unité
            if self.carte.Obstacle[r[0],r[1]] == 0:
                self.Joueur1.assigner_unites(i,[r[0],r[1]])
                self.liste_unites.append(self.Joueur1.unites[-1])
                self.carte.Obstacle[r[0],r[1]] = 1
                i = i+1

        j = 1        #Set unites Player2     
        while j<=4: 
            r = [random.randint(6,9),random.randint(11,14)]
            if self.carte.Obstacle[r[0],r[1]] == 0:
                self.Joueur2.assigner_unites(j,[r[0],r[1]])
                self.liste_unites.append(self.Joueur2.unites[-1])
                self.carte.Obstacle[r[0],r[1]] = 1
                j = j+1            
                
        return self.liste_unites


# Création des Coup (Classe Coup du programme)
    def getCoup(self,unite,carte):
        #En entrée, unite de classe Unité, et carte de classe Map
        return PD.Coup(unite,carte)


# Retourne les postions de déplacement valide pour une unité 'unit' et une map 'Carte' données.    
    def getDeplacementValide(self,unit,Carte):
        return(unit.CaseDeplacable_calcul(Carte))


# Changement de Tour pour les joueurs        
    def getTour_de(self):        
        if self.Tour_de == self.Joueur1:
            self.Tour.nouveautour(self,self.Joueur1,self.Joueur2)
            return(self.Joueur2)            
        elif self.Tour_de == self.Joueur2:
            self.Tour.nouveautour(self,self.Joueur1,self.Joueur2)
            return(self.Joueur1)


# Lancer une nouvelle partie (Quand on appuit sur le bouton 'Nouvelle Partie')   
    def new_game(self,nom_joueur1, nom_joueur2):
        
        self.WM = self.getWallManager(PD.WallManager(self.w,self.h))
        self.carte = self.getMap(PD.Map())
        self.carte.NumberMap = self.NumberMap
        self.carte.SetMap()
        [self.Joueur1,self.Joueur2] = self.set_players(nom_joueur1,nom_joueur2)
        self.liste_unites = self.getUnites()
        
        self.carte.Maj([self.Joueur1,self.Joueur2])
        self.Tour = self.getTour()
        self.curseur = self.getCursor()

        self.Tour_de = self.Joueur1
        self.MapMaj()
        
        if self.view:
            self.view.Delete_All_Persos()
            self.view.RESET()


# Mettre en place le Jeu. Cette fonction est utilisé pour initialiser le jeu
#lorsqu'on démarre le jeu. Par défaut, les joueurs sont des hummains. Les unités
#sont pas crées
    def set_game(self,w = 15, h = 10) :
        # w et h sont les tailles de la map. Par défaut: 15*10
        self.w = w
        self.h = h
        self.WM = self.getWallManager(PD.WallManager(self.w,self.h))
        self.carte = self.getMap(PD.Map())
        self.carte.SetMap()
        [self.Joueur1,self.Joueur2] = self.set_players('Player1','Player2')
        self.carte.Maj([self.Joueur1,self.Joueur2])
        self.MapMaj()

# Mettre à jour tout: Les listes des unités des joueurs, la map, ainsi que les
#fenêtres d'information (Messages, Info, PV, etc.. )
    def MapMaj(self):        
        self.Joueur1.MajArmee()
        self.Joueur2.MajArmee()
        self.carte.Maj([self.Joueur1,self.Joueur2])
        self.Victoire = PD.Tour.victoire(self,self.Joueur1,self.Joueur2)  
        if self.startparam:
            self.startparam.refresh() 
        if self.startmessage:
            self.startmessage.refresh()
        if self.startinfo:
            self.CurseurInfo_refresh()        
        if self.Victoire:
            self.Keyboard = False
            
            
# Mise à jour des infos sur la position du curseur. Affiché en bas du fenêtre 
#du jeu.
    def CurseurInfo_refresh(self):
        self.curseurinfo = "-------- Fire Emblem 1.1 by Yixin & Vignesh --------"
        nomtypeterrain = {0:"plaine",1:"foret",2:"montagne",-1:"obstacle"}
        deplacement = {True:"Oui",False:"Non"}
        attaque = {True:"Oui",False:"Non"}
        unite = None
        
        if self.Tour_de.nom.startswith('B') == True or self.Tour_de.nom.startswith('A') == True :
            if self.view.perso_selected:
                self.curseurinfo = "L'IA est en train de réfléchir... hmm, je vais jouer l'unité {}  (PV: {}, Dégats: {} (+{}))".format(self.view.perso_selected.nom,self.view.perso_selected.PV,self.view.perso_selected.degat,self.carte.terrain[self.view.perso_selected.position[0],self.view.perso_selected.position[1]])
            else:
                self.curseurinfo = "L'IA est en train de réfléchir... "
        else:
            if self.carte.PositionsPersos[self.curseur.position[0],self.curseur.position[1]] == 0:
                self.curseurinfo = "Terrain: {}  -  Occupation: Non occupée".format(nomtypeterrain[self.carte.terrain[self.curseur.position[0],self.curseur.position[1]]])
            else:
                for u in self.liste_unites:
                    if u.position == self.curseur.position:
                        unite = u
                if unite.Appartenance == self.Tour_de.nom:
                    self.curseurinfo = "Terrain: {}  -  Occupation: Unité  {}  de  {}  -  PV: {}, Dégats: {} (+{})  -  Déplacement: {},  Combat: {}".format(nomtypeterrain[self.carte.terrain[self.curseur.position[0],self.curseur.position[1]]],unite.nom,unite.Appartenance,unite.PV,unite.degat,self.carte.terrain[self.curseur.position[0],self.curseur.position[1]],deplacement[unite.pasencoredéplacée],attaque[unite.pasencorecombattu])
                else:
                    self.curseurinfo = "Terrain: {}  -  Occupation: Unité  {}  de  {}, PV: {}, Dégats: {} (+{})".format(nomtypeterrain[self.carte.terrain[self.curseur.position[0],self.curseur.position[1]]],unite.nom,unite.Appartenance,unite.PV,unite.degat,self.carte.terrain[self.curseur.position[0],self.curseur.position[1]])

        if self.startinfo:
            self.startinfo.refresh()
            

        
# Fermer la fenêtre du jeu.        
    def quit(self):
        if self.main_window:
            self.main_window.close()

        

        
        



        