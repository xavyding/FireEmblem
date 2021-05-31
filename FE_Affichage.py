# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:59:26 2017

@author: Vignesh
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import scipy.misc as sc
#import pdb

import numpy as np
from FE_Controleur import *
from random import randint
#import functools; 
"""
ItemWall : Item représentant un mur
"""



###############Fonctions utiles##################
class Image(QImage):
    def __init__(self,FileName):
        QImage.__init__ (self, FileName)
        
class Brush(QBrush):
    def __init__(self,image):
        QBrush.__init__ (self, image)

###############Partie Graphique##################



s=100 #coefficient multiplicateur de la taille des cases dans la fenêtre et donc des positions des objets


#Classe LaSceneGlobale : Elle possède les attributs de QGraphicsScene et permet
#la création d'objets graphiques sur celle-ci. Elle permet de définir l'arrère plan du jeu, qui réprésente la carte
class LaSceneGlobale(QGraphicsScene):
    def __init__(self,parent,WM,controlleur): 
#       WM : objet de type WallManager
#       controlleur : objet de type FEController
        super().__init__(parent)
        self.controlleur = controlleur

        self.create_scene() # permet de creer l'objet QRectF et qui aura ses propriétés
        self.scene=self.sceneRect() #on prend la zone rectangulaire de l'objet QRectF

 

 #je remplis chaque case vide avec une texture d'un arrière plan découpé au préalable.   
    def create_scene(self):
        self.setSceneRect(0, 0, self.controlleur.w * s, self.controlleur.h * s)
        img=Image('Texture/FEC00.png')
        newimg=img.scaledToHeight (s, 1)
        brush=Brush(newimg)
        
        for wall in self.controlleur.WM.get_walls():
            x, y = wall.pos.x, wall.pos.y
            
            if self.controlleur.carte.NumberMap == 1:
                img=Image('Texture/Map/6/FEC6/FEC6 [www.imagesplitter.net]-{y}-{x}.png'.format(x=x,y=y))
                newimg=img.scaledToHeight (s, 0)
                brush=Brush(newimg)
                self.addRect(x * s, y * s, s, s, QPen(QColor(100, 100, 100)), brush )
            
            elif self.controlleur.carte.NumberMap == 2:
                img=Image('Texture/Map/8/FEC8/FEC8 [www.imagesplitter.net]-{y}-{x}.png'.format(x=x,y=y))
                newimg=img.scaledToHeight (s, 0)
                brush=Brush(newimg)
                self.addRect(x * s, y * s, s, s, QPen(QColor(100, 100, 100)), brush )


# Classe qui gère l'affichage graphique du curseur et son déplacement              
class CursorRed(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.gif_cursor = QLabel()        
        self.cursor = QGraphicsProxyWidget()
        self.cursor.setWidget(self.gif_cursor)
        self.addToGroup(self.cursor)        
        self.movie = QMovie("Texture/Curseur/CursorRed.gif")
        self.gif_cursor.setMovie(self.movie)
        self.gif_cursor.setStyleSheet("background:transparent;")
        self.movie.start()


# Classe qui gère l'affichage graphique des cases de déplacement 
#d'une unité à partir d'une position        
class CaseDeplacementDispo(QGraphicsItemGroup):
    def __init__(self,POSITION):
#       POSITION : objet de type liste de taille (1,2) contenant les coordonnées 
#       à partir desquelles le déplacement d'une unité va se faire.
        super().__init__()
        self.pos = POSITION
        self.gif_case = QLabel()           
        self.case = QGraphicsProxyWidget()
        self.case.setWidget(self.gif_case)
        self.addToGroup(self.case)        
        self.movie = QMovie("Texture/Curseur/Caseorange.gif")
        self.gif_case.setMovie(self.movie)
        self.gif_case.setStyleSheet("background:transparent;")
        self.movie.start()


#Classe gérant l'affichage graphique d'une unité avec différents états : 
# non sélectionnée NS, en attente (stand) Std, déplacement  à gauche droite bas et haut (L,R,D,U)
# attaque à gauche droite bas et haut (LA,RA,DA,UA), subissant des dégâts (DM) et morte DeadFade
class Personnages(QGraphicsItemGroup):
    def __init__(self,controlleur,PD_UNITE):
        
        super().__init__()
        self.controlleur = controlleur
        self.PPD = PD_UNITE #Perso Programme decembre
        self.gif_perso = QLabel()
        self.etat = None
        self.choisir_etat(-1)
        self.perso = QGraphicsProxyWidget()
        self.perso.setWidget(self.gif_perso)
        self.gif_perso.setStyleSheet("background:transparent;")
        
        self.addToGroup(self.perso)
        
    def __repr__(self):
        return 'Personnage{}'.format(self.PPD.nom)
    
    def choisir_etat(self,k):
        #permet de choisir quelle animation on veut pour un perso, selon que 
        #l'on voudra faire action à gauche, à droite, en haut ou en bas

        if k == -2:
            #stand
            self.etat = -2
            self.movie = QMovie("Texture/Persos/DeadFade.gif")
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()

        if k == -1:
            #stand, not selected
            self.etat = -1
            self.movie = QMovie("Texture/Persos/{}NS_PX{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
            
        if k == 0:
            #stand
            self.etat = 0
            self.movie = QMovie("Texture/Persos/{}Std{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()            
        elif k == 1:
            #right
            self.etat = 1
            self.movie = QMovie("Texture/Persos/{}R{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()            
        elif k == 2:
            #left
            self.etat = 2
            self.movie = QMovie("Texture/Persos/{}L{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()        
        elif k == 3 :
            #down
            self.etat = 3
            self.movie = QMovie("Texture/Persos/{}D{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()        
        elif k == 4 :
            #up
            self.etat = 4
            self.movie = QMovie("Texture/Persos/{}U{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
        elif k == 5 :
            #rightAttack
            self.etat = 5
            self.movie = QMovie("Texture/Persos/{}RA{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
        elif k == 6 :
            #leftAttack
            self.etat = 6
            self.movie = QMovie("Texture/Persos/{}LA{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
        elif k == 7 :
            #downAttack
            self.etat = 7
            self.movie = QMovie("Texture/Persos/{}DA{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
        elif k == 8 :
            #upAttack
            self.etat = 8
            self.movie = QMovie("Texture/Persos/{}UA{}.gif".format(self.PPD.nom[:3],self.PPD.Appartenance[-1]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()
        elif k == 9 :
            #Damaged
            self.etat = 9
            self.movie = QMovie("Texture/Persos/{}DM.gif".format(self.PPD.nom[:3]))
            self.gif_perso.setMovie(self.movie)
            self.gif_perso.setStyleSheet("background:transparent;")
            self.movie.start()





# Classe principale gérant l'intéraction entre tous les objets graphiques 
#(LaSceneglobale, Personnages, Curseur, CaseDeplacementDispo). On décrit cette classe (très longue)
# en plusieurs parties sanctionnées d'un titre représentatif des fonctions et de leur utilité
class ViewGAME(QGraphicsView):
    def __init__(self,parent,controlleur,LISTE_PERSO):
        super().__init__(parent)       
#       LISTE_PERSO : objet de type 'list' contenant des objets de type Personnages. 
#                     Elle contient les Personnages des deux Joueurs
        self.setWindowTitle('Fire Emblem 2.0 - By: Vignesh & Yixin')
        self.controlleur = controlleur
        self.controlleur.Personnages = []        
        self.chemin = []
        self.PossibleCases = []
        self.Case = None
        self.Memory_perso = None
        self.Memory_case = None               
        self.scene=LaSceneGlobale(self,self.controlleur.WM,self.controlleur)         
        self.Cursor = CursorRed()
        self.perso_selected = False
        self.setScene(self.scene)        
        self.EnDeplacement = False
        self.aAttaque = False        
        self.controlleur.view = self
        self.timer = QTimer()         

#Mise en place des objets Personnages dans classe LaSceneGlobale ( = la scene)       
    def init_perso(self,LISTE_PERSO):

        for self.P in LISTE_PERSO:    
            self.P.choisir_etat(-1)
            self.scene.addItem(self.P)
            self.controlleur.Personnages.append(self.P)
            self.P.setZValue(1)
            self.P.setPos(self.P.PPD.position[1]*s,self.P.PPD.position[0]*s)

# Affichage des deplacement possibles à une position dans la scène donnée, s'il y a un objet de type Personnage
# Ajout alors si c'est le case des objets de type CaseDeplacementDispo
    def show_possiblemove(self):
        if self.perso_selected == self.Memory_perso and self.perso_selected.pasencoredéplacée == True:
            #Skip calcul
            self.PossibleCases = self.Memory_case
        else:
            TrueFalseMatrix = self.controlleur.getDeplacementValide(self.perso_selected, self.controlleur.carte)
            self.Memory_perso = self.perso_selected
            for i in range(np.shape(TrueFalseMatrix)[0]):
                for j in range(np.shape(TrueFalseMatrix)[1]):
                    if TrueFalseMatrix[i,j]:
                        self.PossibleCases.append(CaseDeplacementDispo((i,j)))
            self.Memory_case = self.PossibleCases
            
        for self.Case in self.PossibleCases:
            self.scene.addItem(self.Case)
            self.Case.setZValue(0)
            self.Case.setPos(self.Case.pos[1]*s,self.Case.pos[0]*s)

              
# Retire de la scene les objets de type CaseDeplacementDispo    
    def hide_possiblemove(self):
        for C in self.PossibleCases:
            self.scene.removeItem(C)
        self.PossibleCases = []

#####################################################################################################################################################
#----------------------------------------------------------------------- DEPLACEMENT -------------------------------------------------------       
#####################################################################################################################################################           

# Utilisation des animations de deplacement lorsque l'objet de type Personnage est déplacé 
#dans la scéne d'une position initiale à une position finale
    def deplacement(self,chemin,perso):
#       chemin : objet de type 'list' contenant les coordonnées matricielles 
#               de chaque case sur le chemin calculé de la position initale à la position finale
#       perso : objet de type Unité qui effectue le déplacement
        self.chemin = chemin

        if self.chemin:  #Si chemin n'est pas false ou liste vide 
            self.a = int(self.chemin[0][1]*s)
            self.b = int(self.chemin[0][0]*s)        
            self.x = int(perso.position[1]*s)
            self.y = int(perso.position[0]*s)        
            self.EnDeplacement = True

            for P in self.controlleur.Personnages:
                if P.PPD == perso:
                    self.perso_selected = perso
                    self.P = P
                    
    
            if self.a-self.x < 0:     #x-
                self.P.choisir_etat(2)
                self.timer = QTimer()
                self.timer.timeout.connect(self.deplacerXMoins)                
            elif  self.a-self.x > 0:  #x+
                self.P.choisir_etat(1)
                self.timer = QTimer()
                self.timer.timeout.connect(self.deplacerXPlus)
            elif  self.b-self.y < 0:  #y-
                self.P.choisir_etat(4)
                self.timer = QTimer()
                self.timer.timeout.connect(self.deplacerYMoins)
            elif  self.b-self.y > 0:  #y+-
                self.P.choisir_etat(3)
                self.timer = QTimer()
                self.timer.timeout.connect(self.deplacerYPlus)
            else: #Not Moving (Movement finished)
                self.P.choisir_etat(0)
                self.EnDeplacement = False
                self.MajAffichage()  #Maj de la carte
          
                self.timer = QTimer()
                self.timer.timeout.connect(self.deplacerNone)            
                
        else: #Not Moving 
            self.P.choisir_etat(0)
            self.EnDeplacement = False
            self.MajAffichage()  #Maj de la carte
            self.timer = QTimer()
            self.timer.timeout.connect(self.deplacerNone) 
            self.controlleur.isFinished = True
        self.timer.start(100)
        
    def deplacerXMoins(self):
        if abs(self.a-self.x)>0 :
            self.x-=10
            self.P.setPos(self.x,self.y) #fonction définie ds QGraphicsItem
        if abs(self.a-self.x) == 0: 
            self.chemin = self.chemin[1:]                       
            self.perso_selected.position = [int(self.y/s),int(self.x/s)]
            self.deplacement(self.chemin,self.perso_selected)        
    def deplacerXPlus(self):
        if abs(self.a-self.x)>0 :
            self.x+=10       
            self.P.setPos(self.x,self.y)
        if abs(self.a-self.x) == 0:            
            self.chemin = self.chemin[1:]                       
            self.perso_selected.position = [int(self.y/s),int(self.x/s)]
            self.deplacement(self.chemin,self.perso_selected)           
    def deplacerYMoins(self):
        if abs(self.b-self.y)>0 :
            self.y-=10
            self.P.setPos(self.x,self.y)
        if abs(self.b-self.y) == 0:            
            self.chemin = self.chemin[1:]                       
            self.perso_selected.position = [int(self.y/s),int(self.x/s)]
            self.deplacement(self.chemin,self.perso_selected)        
    def deplacerYPlus(self):
        if abs(self.b-self.y)>0 :
            self.y+=10
            self.P.setPos(self.x,self.y)        
        if abs(self.b-self.y) == 0:            
            self.chemin = self.chemin[1:]                       
            self.perso_selected.position = [int(self.y/s),int(self.x/s)]
            self.deplacement(self.chemin,self.perso_selected)
    def deplacerNone(self): 
        self.timer.stop()
        self.P.setPos(self.x,self.y)
        if self.perso_selected:
            if self.perso_selected.pasencoredéplacée and self.controlleur.Tour_de.nom.startswith('B') == False and self.controlleur.Tour_de.nom.startswith('A') == False:
                self.show_possiblemove()
        
        #Jouer l'IA (si c'est le tour d'IA)
        if self.controlleur.Tour_de.nom.startswith('B') == True or self.controlleur.Tour_de.nom.startswith('A') == True :
            self.IA_Combat()
#####################################################################################################################################################
#--------------------------------------------------------   COMBAT    -----------------------------------------------------------------------------  
#####################################################################################################################################################



# Utilisation des animations de combat lorsque l'objet de type Personnage 
# est utilisé pour animer une attaque sur un autre Personnage

            
    def combat(self,a,b,perso):
#        a,b : objets de type int contenant les coordonnées matricielles du Personnage qui subit l'attaque 
#        perso : objet de type Unité qui effectue l'attaque
#        

        self.a = int(a*s)
        self.b = int(b*s)        
        self.x = int(perso.position[1]*s)
        self.y = int(perso.position[0]*s)        
        
        for P in self.controlleur.Personnages:
            if P.PPD == perso:
                self.perso_selected = perso
                self.P = P      
        
        if self.a-self.x < 0 and self.aAttaque == False:     #x-
            self.P.choisir_etat(6)
            self.timer = QTimer()
            self.timer.timeout.connect(self.AttaquerXMoins)            
        elif  self.a-self.x > 0 and self.aAttaque == False:  #x+
            self.P.choisir_etat(5)
            self.timer = QTimer()
            self.timer.timeout.connect(self.AttaquerXPlus)
        elif  self.b-self.y < 0 and self.aAttaque == False:  #y-
            self.P.choisir_etat(8)
            self.timer = QTimer()
            self.timer.timeout.connect(self.AttaquerYMoins)
        elif  self.b-self.y > 0 and self.aAttaque == False:  #y+-
            self.P.choisir_etat(7)
            self.timer = QTimer()
            self.timer.timeout.connect(self.AttaquerYPlus)
        else: #Not Attacking
            self.P.choisir_etat(0)
            self.aAttaque = False
            self.MajAffichage()  #Maj de la carte
            self.timer = QTimer()
            self.timer.timeout.connect(self.AttaquerNone)
        self.timer.start(1000)
                        
        
    def AttaquerXMoins(self):
        if abs(self.a-self.x) == 100 and self.aAttaque == False:
            self.aAttaque =True
            self.combat(self.a/s,self.b/s,self.perso_selected)        
    def AttaquerXPlus(self):
        if abs(self.a-self.x) == 100 and self.aAttaque == False:
            self.aAttaque =True
            self.combat(self.a/s,self.b/s,self.perso_selected)          
    def AttaquerYMoins(self):
        if abs(self.b-self.y) == 100 and self.aAttaque == False:
            self.aAttaque =True
            self.combat(self.a/s,self.b/s,self.perso_selected)     
    def AttaquerYPlus(self):
 
        if abs(self.b-self.y) == 100 and self.aAttaque == False:            
            self.aAttaque =True
            self.combat(self.a/s,self.b/s,self.perso_selected)

    def AttaquerNone(self):
        self.timer.stop()        
        for P in self.controlleur.Personnages:
            if P.etat ==9:
                P.choisir_etat(-1)
        if self.perso_selected:
            if self.perso_selected.pasencoredéplacée and self.controlleur.Tour_de.nom.startswith('B') == False and self.controlleur.Tour_de.nom.startswith('A') == False:
                self.show_possiblemove()
                
        #Jouer l'IA (si c'est le tour d'IA)        
        if self.controlleur.Tour_de.nom.startswith('B') == True or self.controlleur.Tour_de.nom.startswith('A') == True :
            self.timer.stop()
            self.IA_Deselection()
            
            
#####################################################################################################################################################
#---------------------------------------------------------------------------- Mise à Jour de la Scene------------------------------------------------------------------
#####################################################################################################################################################
 

           
# change l'animation d'un objet de type Personnage en une animation de 'mort' si celui-ci n'a plus de PV        
    def MajAffichage(self):
        for P in self.controlleur.Personnages:
            if P.PPD.PV <= 0 :
                P.choisir_etat(-2)
        self.controlleur.MapMaj()


# Retire l'objet Personnage de la scène si l'objet possède l'animation 'mort'        
    def RemoveDead(self):
        for P in self.controlleur.Personnages :
            
            if P.etat == -2 :
                self.controlleur.Personnages.remove(P)
                self.scene.removeItem(P)

#  L'objet de type Personnage Revient à l'état Stand                 
    def change_etat(self,PERSO):
        PERSO.choisir_etat(0)

# Enlève l'objet Curseur si c'est au tour du Joueur IA de jouer. Sinon l'affiche pour le Joueur Humain        
    def show_hide_cursor(self,controlleur):
        if controlleur.Keyboard:
            self.scene.addItem(self.Cursor)
            self.Cursor.setZValue(2)
            self.Cursor.setPos(self.xcursor,self.ycursor)            
        else:
            self.scene.removeItem(self.Cursor)
        

#####################################################################################################################################################
#------------------------------------------------- Partie Gestion Graphique pour l'IA-----------------------------------------------------------------
#####################################################################################################################################################


#    Effectue les représentations graphiques des actions de l'IA
    def PlayBOT(self):
        if not(self.controlleur.Victoire):
            self.controlleur.Keyboard = False
            self.show_hide_cursor(self.controlleur)
            if self.controlleur.Tour_de.tourfini == False:
                self.RemoveDead()
                self.IA_Deplacement()
                
            else:
                self.controlleur.Tour_de.tourfini = False
                self.IA_Tour()
            
 
# Mise en place des animations de déplacement pour l'IA selon qu'elle soit aléatoire ou non.       
    def IA_Deplacement(self):
 
        if self.controlleur.Tour_de.nom.startswith('B') == True : 
            self.perso_selected = self.controlleur.Tour_de.Choix_unite_IA(self.controlleur.Joueur1.unites + self.controlleur.Joueur2.unites)

            if self.perso_selected:
                chemin = self.controlleur.Tour_de.deplacement_IA(self.perso_selected)
                self.deplacement(chemin,self.perso_selected)
            
        elif self.controlleur.Tour_de.nom.startswith('A') == True :
            self.perso_selected = self.controlleur.Tour_de.Choix_unite_IA_Random()
            if self.perso_selected:
                chemin = self.controlleur.Tour_de.deplacement_IA_Random(self.perso_selected)
                self.deplacement(chemin,self.perso_selected)
        
        self.controlleur.CurseurInfo_refresh()


# Mise en place des animations de dcombat pour l'IA selon qu'elle soit aléatoire ou non.       
    def IA_Combat(self):        
        if self.controlleur.Tour_de.nom.startswith('B') == True : 
            Focus =  self.controlleur.Tour_de.combat_IA(self.perso_selected,self.controlleur.Joueur1.unites + self.controlleur.Joueur2.unites)
            if Focus:
                self.combat(Focus.position[1],Focus.position[0],self.perso_selected)
                
                for P in self.controlleur.Personnages:
                    if P.PPD == Focus:
                        self.P=P
                        self.P.choisir_etat(9)
                for P in self.controlleur.Personnages:
                    if P.PPD ==self.perso_selected:
                        self.P=P                
            else:
                self.AttaquerNone()
                
                
        elif self.controlleur.Tour_de.nom.startswith('A') == True :
            Focus =  self.controlleur.Tour_de.combat_IA_Random(self.perso_selected,self.controlleur.Joueur1.unites + self.controlleur.Joueur2.unites)
            if Focus:
                self.combat(Focus.position[1],Focus.position[0],self.perso_selected)
                
                for P in self.controlleur.Personnages:
                    if P.PPD == Focus:
                        self.P=P
                        self.P.choisir_etat(9)
                for P in self.controlleur.Personnages:
                    if P.PPD ==self.perso_selected:
                        self.P=P                
            else:
                self.AttaquerNone()


# Montre l'animation de déselection d'une unité par l'IA
    def IA_Deselection(self):

        for P in self.controlleur.Personnages:
            if P.PPD.PV >0:
                P.choisir_etat(-1)
        self.perso_selected = False
        self.PlayBOT()

# Définit le tour de l'IA. Elle joue si l'objet Tour indique qu'il s'agit de son tour, sinon elle repasse la main au joueur adverse                       
    def IA_Tour(self):
        self.controlleur.Tour_de = self.controlleur.getTour_de()
        self.controlleur.MapMaj()
        if self.controlleur.Tour_de.nom.startswith('B') == True or self.controlleur.Tour_de.nom.startswith('A') == True :
            self.PlayBOT()
        else:
            self.controlleur.Keyboard = True
            self.show_hide_cursor(self.controlleur)



#####################################################################################################################################################
#--------------------------------------------------- Partie Gestion Graphique pour le Joueur Humain--------------------------------------------------------------
#####################################################################################################################################################

#Le jeu est utilisé via des les touches du clavier uniquement.
#Details des touches  :

#            - flèches du clavier : déplacement du curseur           
#            - A : attaquer la position où le curseur se trouve (ne marche que si une des unités ennemies s'y trouve)
#            - S : sélectionner /déselectionner la position où le curseur se trouve (ne marche que si une de vos unités s'y trouve)
#            - Espace : Confirmer le déplacement, après avoir sélectionné une unité, à la position où se trouve le curseur
#            - I : donne des informations à la position où se trouve le curseur (occupation par une unité, type de terrain)  (obsolète?)
#            - T : passer le Tour à l'adversaire, à faire obligatoirement quand le Joueur a fini de jouer ce qu'il voulait 
#                  (qu'il reste des unités jouables ou non)
    def keyPressEvent(self, event):
        if self.controlleur.Keyboard: #Permet l'utilisation du clavier (à désactiver au tour des Bots)
            touche = event.key()
        else:
            touche = None
        
        if touche != Qt.Key_Left and touche != Qt.Key_Right and touche != Qt.Key_Up and touche != Qt.Key_Down:
            self.RemoveDead()
            self.hide_possiblemove() if (self.perso_selected != False and touche !=Qt.Key_S) else None
        
        if touche == Qt.Key_Space and self.EnDeplacement == False and self.perso_selected != False and self.perso_selected.pasencoredéplacée==True: #Lancer déplacement
            self.deplacement(self.controlleur.getCoup(self.perso_selected,self.controlleur.carte).deplacement_return(int(self.ycursor/s), int(self.xcursor/s)),self.perso_selected)  #effectuer le déplacement
            
        elif touche == Qt.Key_Left and self.xcursor>=100: #Bouger curseur
            self.xcursor -= 100
            self.controlleur.curseur.deplacer_curseur(int(self.ycursor/s),int(self.xcursor/s))
            self.controlleur.CurseurInfo_refresh()
            self.Cursor.setPos(self.xcursor,self.ycursor)            
        elif touche == Qt.Key_Right and self.xcursor <= (np.shape(self.controlleur.carte.terrain)[1]-2)*s: #Bouger curseur
            self.xcursor += 100
            self.controlleur.curseur.deplacer_curseur(int(self.ycursor/s),int(self.xcursor/s))
            self.controlleur.CurseurInfo_refresh()
            self.Cursor.setPos(self.xcursor,self.ycursor) 
        elif touche == Qt.Key_Up and self.ycursor>=100: #Bouger curseur
            self.ycursor -= 100
            self.controlleur.curseur.deplacer_curseur(int(self.ycursor/s),int(self.xcursor/s))
            self.controlleur.CurseurInfo_refresh()
            self.Cursor.setPos(self.xcursor,self.ycursor)
        elif touche == Qt.Key_Down and self.ycursor <= (np.shape(self.controlleur.carte.terrain)[0]-2)*s: #Bouger curseur
            self.ycursor += 100
            self.controlleur.curseur.deplacer_curseur(int(self.ycursor/s),int(self.xcursor/s))
            self.controlleur.CurseurInfo_refresh()
            self.Cursor.setPos(self.xcursor,self.ycursor)  
            
        elif touche == Qt.Key_T and self.perso_selected == False and self.aAttaque == False: #changer de joueur 
            
            self.controlleur.Tour_de = self.controlleur.getTour_de()
            self.controlleur.MapMaj()            
            if self.controlleur.Tour_de.nom.startswith('B') == True or self.controlleur.Tour_de.nom.startswith('A') == True :
                self.PlayBOT()
            
        elif touche == Qt.Key_I:
            self.controlleur.curseur.info()

      
        elif touche == Qt.Key_S and self.EnDeplacement == False: #Selectionner une unité
            if self.controlleur.curseur.selectionner(self.controlleur.Tour_de) != False:

                for P in self.controlleur.Personnages:
                    if P.PPD == self.controlleur.curseur.selectionner(self.controlleur.Tour_de):                        
                        self.P = P                       
                        if self.P.etat ==-1: #Selection
                            for P_ex in self.controlleur.Personnages :
                                if P_ex.etat != 1:
                                    P_ex.choisir_etat(-1)
                                    self.hide_possiblemove()
                            self.perso_selected = self.P.PPD
                            self.x = int(self.perso_selected.position[1]*s)
                            self.y = int(self.perso_selected.position[0]*s)                            
                            self.show_possiblemove()                    
                            self.P.choisir_etat(0)

                        else:#Déselection

                            self.hide_possiblemove()                                                 
                            self.perso_selected = False
                            self.P.choisir_etat(-1)
        
        elif touche == Qt.Key_A and self.EnDeplacement == False and self.perso_selected != False and self.perso_selected.pasencorecombattu == True: #Lancer combat
            
            if self.controlleur.Tour_de ==self.controlleur.Joueur1:
                if self.controlleur.curseur.selectionner(self.controlleur.Joueur2) != False:
                    [b,a] = self.controlleur.getCoup(self.perso_selected,self.controlleur.carte).combat_return(self.controlleur.curseur.selectionner(self.controlleur.Joueur2))                        
                    self.combat(a,b,self.perso_selected)  #afficher le combat           
                    for P in self.controlleur.Personnages:
                        if P.PPD ==self.controlleur.curseur.selectionner(self.controlleur.Joueur2):
                            self.P=P
                            self.P.choisir_etat(9)
                    for P in self.controlleur.Personnages:
                        if P.PPD ==self.perso_selected:
                            self.P=P
                else:
                    self.AttaquerNone()
                                                   
            elif self.controlleur.Tour_de ==self.controlleur.Joueur2:
                if self.controlleur.curseur.selectionner(self.controlleur.Joueur1) != False:
                    [b,a] = self.controlleur.getCoup(self.perso_selected,self.controlleur.carte).combat_return(self.controlleur.curseur.selectionner(self.controlleur.Joueur1))
                    self.combat(a,b,self.perso_selected)  #afficher le combat           
                    for P in self.controlleur.Personnages:
                        if P.PPD ==self.controlleur.curseur.selectionner(self.controlleur.Joueur1):
                            self.P=P
                            self.P.choisir_etat(9)
                    for P in self.controlleur.Personnages:
                        if P.PPD ==self.perso_selected:
                            self.P=P
                else:
                    self.AttaquerNone()

            
        elif touche == Qt.Key_Backspace and self.EnDeplacement == False and self.aAttaque == False:
            for P in self.controlleur.Personnages:
                if P.PPD.PV >0:
                    P.choisir_etat(-1)
            self.perso_selected = False
            self.RemoveDead()

#####################################################################################################################################################
#--------------------------------------------------------------------Remise à zéro du jeu------------------------------------------------------------
#####################################################################################################################################################
    def Delete_All_Persos(self):
        self.scene.removeItem(self.Cursor)
        for P in self.controlleur.Personnages:
            self.scene.removeItem(P)

      
    def RESET(self):
        print('RESET')
        
        self.timer.stop()
        self.scene.create_scene() 
   

        self.xcursor = 0
        self.ycursor = 0 
        self.scene.addItem(self.Cursor)
        self.Cursor.setZValue(2)
        self.Cursor.setPos(self.xcursor,self.ycursor)
        
        self.controlleur.Personnages = []    
        LISTE_PERSONNAGE = []

        for u in self.controlleur.liste_unites:
            LISTE_PERSONNAGE +=[Personnages(self.controlleur,u)]

        
        for P in LISTE_PERSONNAGE:    
            P.choisir_etat(-1)
            self.scene.addItem(P)
            self.controlleur.Personnages.append(P)
            P.setZValue(1)
            P.setPos(P.PPD.position[1]*s,P.PPD.position[0]*s)

            
        self.perso_selected = False       
        self.EnDeplacement = False
        self.aAttaque = False

        
        if self.controlleur.Tour_de.nom.startswith('B') == True or self.controlleur.Tour_de.nom.startswith('A') == True :
            self.PlayBOT()
        else:
            self.controlleur.Keyboard = True
            self.show_hide_cursor(self.controlleur)



def test_deplacement_combat():
      
    app = QApplication([])
    controleur = FEController()
    controleur.set_game(10,7)

    mainwindow = ViewGAME(None,controleur,[])
    
    controleur.WM = controleur.getWallManager(PD.WallManager(controleur.w,controleur.h))
    controleur.carte.NumberMap = controleur.NumberMap
    controleur.carte.SetMap()
    [controleur.Joueur1,controleur.Joueur2] = controleur.set_players('Player1','Player2')
#    controleur.liste_unites = controleur.getUnites()
    
    controleur.Joueur1.assigner_unites(3,[3,4])
    controleur.Joueur2.assigner_unites(1,[3,5])
    controleur.liste_unites.append(controleur.Joueur1.unites[-1])
    controleur.liste_unites.append(controleur.Joueur2.unites[-1])
        
    controleur.carte.Maj([controleur.Joueur1,controleur.Joueur2])
    controleur.Tour = controleur.getTour()
    controleur.curseur = controleur.getCursor()

    controleur.Tour_de = controleur.Joueur1
    controleur.MapMaj()
    controleur.view.Delete_All_Persos()
    controleur.view.RESET()
    
    mainwindow.show()
    app.exec()
    

        
def main():
    test_deplacement_combat()
    

        
if __name__ == '__main__': main()