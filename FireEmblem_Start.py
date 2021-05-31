# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 21:45:50 2018

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

from FE_Affichage import *
import ctypes

# Classe Widget permettant d'indiquer le Tour, et la victoire le cas échéant
class MessageWindow(QWidget):
    def __init__(self, parent, controller):
        # En entrée, controller (Classe FEController du contrôleur)
        super().__init__(parent)
        self.control = controller
        self.control.startmessage = self
        self.message = "APPUYER SUR 'Nouvelle Partie' \n POUR COMMENCER UNE PARTIE"
        self.bar = "---------------------------------------------------------------------------------------"
        self.messagelayout = QVBoxLayout()
        self.messagebox = QLabel("{}".format(self.message))
        self.barbox = QLabel("{}".format(self.bar))
        font = QFont()
        font.setPointSize(15);
        font.setBold(True)
        self.messagebox.setFont(font);
        self.messagebox.setAlignment(Qt.AlignCenter)
        self.messagelayout.addWidget(self.messagebox)
        self.messagelayout.addWidget(self.barbox)
        self.setLayout(self.messagelayout)
    
# Mise à jour de l'affichage     
    def refresh(self):
        if self.control.Victoire:
            self.message = "Victoire de: {}".format(self.control.Victoire)
            ctypes.windll.user32.MessageBoxW(0, "Victoire de: {}".format(self.control.Victoire), "GAME OVER", 0)
            self.messagebox.setText(self.message)
        else:            
            if self.control.Tour_de != False:
                self.message = "Tour de: {}".format(self.control.Tour_de.nom)
                self.messagebox.setText(self.message)
                
                
# Classe Widget permettant d'indiquer les informations sur la position du curseur
class InfoWindow(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.control = controller
        self.control.startinfo = self
        self.info = "-------- Fire Emblem 1.1 by Yixin & Vignesh --------"
        self.infolayout = QVBoxLayout()
        self.infobox = QLabel("{}".format(self.info))
        self.infobox.setAlignment(Qt.AlignCenter)
        self.infolayout.addWidget(self.infobox)
        self.setLayout(self.infolayout)
        
# Mise à jour de l'affichage
    def refresh(self):
        self.infobox.setText(self.control.curseurinfo)



# Classe Widget permettant de choisir les paramètres du jeu. C'est à dire:
#les joueurs, la map, lancer une nouvelle partie. Ce Widget montre également
#les PV des unités
class ParametersWindow(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.control = controller
        self.control.startparam = self

        #Choix des joueurs
        types = ['HUMAIN', 'MACHINE', 'ALEATOIRE']
        self.combo_player1 = QComboBox()
        self.combo_player2 = QComboBox()
        for item in types:
            self.combo_player1.addItem(item)
            self.combo_player2.addItem(item)

        self.combo_player1.setCurrentText('HUMAIN')
        self.combo_player2.setCurrentText('HUMAIN')
        
        #Choix de la map
        locations = ['Carte_1', 'Carte_2']        
        self.combo_carte = QComboBox()        
        for loc in locations:
            self.combo_carte.addItem(loc)        
        self.combo_carte.setCurrentText("Carte_1")
        
        layout_joueurs = QFormLayout()
        layout_joueurs.addRow('Joueur 1 ', self.combo_player1)
        layout_joueurs.addRow('Joueur 2', self.combo_player2)
        
        groupbox_joueurs = QGroupBox("Joueurs")
        groupbox_joueurs.setLayout(layout_joueurs)
        
        layout_carte = QFormLayout()
        layout_carte.addRow('Carte ', self.combo_carte)
        
        groupbox_cartes = QGroupBox("Carte")
        groupbox_cartes.setLayout(layout_carte)

        button_newgame = QPushButton("Nouvelle Partie")
        button_newgame.clicked.connect(self.on_new_game)
        
        button_quit = QPushButton("Quitter le jeu")
        button_quit.clicked.connect(self.on_quit)


        layout_actions = QVBoxLayout()
        layout_actions.addWidget(button_newgame)
        layout_actions.addWidget(button_quit)
        
        groupbox_actions = QGroupBox("Actions")
        groupbox_actions.setLayout(layout_actions)

        self.label_score_1 = QLineEdit("-")
        self.label_score_1.setReadOnly(True)
        self.label_score_1.setAlignment(Qt.AlignRight)
        self.label_score_2 = QLineEdit("-")
        self.label_score_2.setReadOnly(True)
        self.label_score_2.setAlignment(Qt.AlignRight)
        
        self.InfosJoueurs = QHBoxLayout()
        
        self.H1 = QVBoxLayout()
        self.H2 = QVBoxLayout()
        self.H1Joueur = QHBoxLayout()
        self.H2Joueur = QHBoxLayout()
        self.H1label = QLabel("Player 1")
        self.H2label = QLabel("Player 2")
        self.H1Joueur.addWidget(self.H1label)
        self.H2Joueur.addWidget(self.H2label)
        self.H1.addLayout(self.H1Joueur)
        self.H2.addLayout(self.H2Joueur)
        
        self.HEtats = QVBoxLayout()
        self.H1Etats = QHBoxLayout()
        self.H2Etats = QHBoxLayout()
        
        self.H11 = QVBoxLayout()
        self.H12 = QVBoxLayout()
        self.H21 = QVBoxLayout()
        self.H22 = QVBoxLayout()
        self.H11label = QLabel("Unités")
        self.H12label = QLabel("PV")
        self.H21label = QLabel("Unités")
        self.H22label = QLabel("PV")
        
        self.H11.addWidget(self.H11label)
        self.H12.addWidget(self.H12label)
        self.H21.addWidget(self.H21label)
        self.H22.addWidget(self.H22label)
        
        self.H1Etats.addLayout(self.H11)
        self.H1Etats.addLayout(self.H12)
        self.H2Etats.addLayout(self.H21)
        self.H2Etats.addLayout(self.H22)
        
        self.H1.addLayout(self.H1Etats)
        self.H2.addLayout(self.H2Etats)
        
        self.details1 = QHBoxLayout()
        self.details2 = QHBoxLayout()
        
        self.V11 = QVBoxLayout()
        self.V12 = QVBoxLayout()
        self.V21 = QVBoxLayout()
        self.V22 = QVBoxLayout()
        
        self.V11label = []
        self.V12label = []
        self.V21label = []
        self.V22label = []
        
        for k in self.control.Joueur1.unites:
            self.V11label.append(QLabel(k.nom,self))
            self.V12label.append(QLabel(" {a} / {b}".format(a = k.PV, b = k.PVmax),self))
            
        for k in self.control.Joueur2.unites:
            self.V21label.append(QLabel(k.nom,self))
            self.V22label.append(QLabel(" {a} / {b}".format(a = k.PV, b = k.PVmax),self))
#            
        for k in self.V11label:
            self.V11.addWidget(k)            
        for k in self.V12label:
            self.V12.addWidget(k)        
        for k in self.V21label:
            self.V21.addWidget(k)        
        for k in self.V22label:
            self.V22.addWidget(k)
            
        self.details1.addLayout(self.V11)
        self.details1.addLayout(self.V12)
        self.details2.addLayout(self.V21)
        self.details2.addLayout(self.V22)
        
        self.H1.addLayout(self.details1)
        self.H2.addLayout(self.details2)
        
        self.InfosJoueurs.addLayout(self.H1)
        self.InfosJoueurs.addLayout(self.H2)
           
        self.groupbox_infosJoueurs = QGroupBox("Infos")
        self.groupbox_infosJoueurs.setLayout(self.InfosJoueurs)

        label_touches_1 = QLabel("Déplacement curseur : flèches clavier")
        label_touches_2 = QLabel("(Dé)Sélectionner : S")
        label_touches_3 = QLabel("Déplacer : Espace")
        label_touches_4 = QLabel("Attaquer : A")
        label_touches_5 = QLabel("Déselectionner tout : Backspace")
        label_touches_6 = QLabel("Finir le tour : T")
        layout_touches = QVBoxLayout()
        layout_touches.addWidget(label_touches_1)
        layout_touches.addWidget(label_touches_2)
        layout_touches.addWidget(label_touches_3)
        layout_touches.addWidget(label_touches_4)
        layout_touches.addWidget(label_touches_5)
        layout_touches.addWidget(label_touches_6)
        groupbox_touches = QGroupBox("Touches")
        groupbox_touches.setLayout(layout_touches)
        layout = QVBoxLayout()
        layout.addWidget(groupbox_joueurs)
        layout.addWidget(self.groupbox_infosJoueurs)
        layout.addWidget(groupbox_cartes)
        layout.addWidget(groupbox_touches)
        layout.addWidget(groupbox_actions)
        layout.addStretch()
        self.setLayout(layout)
        
# Connecter la fonction QUIT du controleur, permettant de quitter le jeu
    def on_quit(self):
        self.control.quit()
        

# Démarer une nouvelle partie
    def on_new_game(self):
        P1 = None
        P2 = None
        
        if self.combo_player1.currentText() == 'HUMAIN':
            P1 = 'Player1'
        elif self.combo_player1.currentText() == 'MACHINE':
            P1 = 'BOT1'
        elif self.combo_player1.currentText() == 'ALEATOIRE':
            P1 = 'Aleatoire1'
            
        if self.combo_player2.currentText() == 'HUMAIN':
            P2 = 'Player2'
        elif self.combo_player2.currentText() == 'MACHINE':
            P2 = 'BOT2'
        elif self.combo_player2.currentText() == 'ALEATOIRE':
            P2 = 'Aleatoire2'
            
        if self.combo_carte.currentText() =='Carte_1':
            self.control.NumberMap = 1
        elif self.combo_carte.currentText() =='Carte_2':
            self.control.NumberMap = 2
      
        self.control.new_game(P1,P2)      
        LISTE_PERSO = []
        
        for u in self.control.liste_unites:
            LISTE_PERSO +=[Personnages(self.control,u)]          
        self.control = self.control.view.controlleur   
        self.control.view.Personnages = LISTE_PERSO
        self.control.view.controlleur.carte.Maj([self.control.Joueur1,self.control.Joueur2])
        


# Mise à jour des affichanges (les PVs)
    def refresh(self):

        if self.V11label==[] and self.V12label == [] and self.V21label == [] and self.V22label == []   :    
            for k in self.control.Joueur1.unites:
                self.V11label.append(QLabel(k.nom,self))
                self.V12label.append(QLabel(" {a}".format(a = k.PV, b = k.PVmax),self))                
            for k in self.control.Joueur2.unites:
                self.V21label.append(QLabel(k.nom,self))
                self.V22label.append(QLabel(" {a} / {b}".format(a = k.PV, b = k.PVmax),self))                    
            for k in self.V11label:
                self.V11.addWidget(k)                
            for k in self.V12label:
                self.V12.addWidget(k)            
            for k in self.V21label:
                self.V21.addWidget(k)            
            for k in self.V22label:
                self.V22.addWidget(k)

        l1 = len(self.V11label)
        l2 = len(self.V21label)
        
        doc = QTextDocument()
        compteur = []
        for k in range(0,l1) :
            compteur.append(0)
        
        for k in range (0,l1):
            doc.setHtml(self.V11label[k].text())
            text = doc.toPlainText()
            for u in self.control.Joueur1.unites:
                
                if u.nom == text:
                    compteur[k]+=1
                    self.V11label[k].setText(u.nom)
                    self.V12label[k].setText(" {a} / {b}".format(a = u.PV, b = u.PVmax))

            if compteur[k] == 0:
                self.V12label[k].setText('-')
      
        compteur = []
        for k in range(0,l2) :
            compteur.append(0)
        
        
        for k in range (0,l2):
            doc.setHtml(self.V21label[k].text())
            text = doc.toPlainText()
            
            for u in self.control.Joueur2.unites:
                if u.nom == text:
                    compteur[k]+=1
                    self.V21label[k].setText(u.nom)
                    self.V22label[k].setText(" {a} / {b}".format(a = u.PV, b = u.PVmax))
            if compteur[k] == 0:
                self.V22label[k].setText('-') 


# Classe permettant de créer la fenêtre globale du jeu
class MainWindow(QMainWindow):
    def __init__(self, controller,LISTE_PERSO):
        #       LISTE_PERSO : objet de type 'list' contenant des objets de type Personnages. 
#                     Elle contient les Personnages des deux Joueurs
        super().__init__()
        self.control = controller
        self.LP = LISTE_PERSO
        self.setWindowTitle("Fire Emblem 1.1 by Yixin & Vignesh")   
        self.view = ViewGAME(self, self.control,self.LP)        
        self.create_central_widget()

    def create_central_widget(self):
        param = ParametersWindow(self, self.control)
        message = MessageWindow(self, self.control)
        info = InfoWindow(self, self.control)
        self.view.controlleur.carte.Maj([self.control.Joueur1,self.control.Joueur2])
        self.control.set_view(self.view)
        self.control.set_main_window(self)
        widget_central = QWidget()        
        layout = QHBoxLayout()
        sous_layout1 = QVBoxLayout()
        sous_layout2 = QVBoxLayout()        
        sous_layout1.addWidget(self.view,4)
        sous_layout1.addWidget(info, 0)
        sous_layout2.addWidget(message,0)        
        sous_layout2.addWidget(param, 0)        
        layout.addLayout(sous_layout1, 0)
        layout.addLayout(sous_layout2, 0)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)
        
        

# Lancer les programmes
def main():
    app = QApplication([])
    control = FEController()
    control.set_game()
    LISTE_PERSO = []    
    mainwindow = MainWindow(control,LISTE_PERSO)
    mainwindow.showFullScreen()
    mainwindow.show()
    app.exec()


if __name__ == '__main__':
    main()

        
        