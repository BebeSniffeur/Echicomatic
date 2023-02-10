############################################################################################################################################################

### images ---> https://www.thespruce.com/most-common-chess-openings-611517 ###

##---------------------------------------------------------------------------##
##-------------------------- Importation des Modules ------------------------##
##---------------------------------------------------------------------------##

from tkinter import *

##---------------------------------------------------------------------------##
##-------------------------- Declaration des classes ------------------------##
##---------------------------------------------------------------------------##

class Cases:
        def __init__(self):
                self.piece=''                       # nom de la piece (cavalier, pion...)
                self.habitee=''                     # couleur de la piece (Blanc, Noir, Vide)
                self.couleurfond=''                 # couleur de la case (Blanc, Noir)
                self.centrex=0
                self.centrey=0

class Positions:                                    # pour calculer sur quelle case on clique
        def __init__(self):
                self.minimum=0
                self.maximum=0
                self.index=0

##---------------------------------------------------------------------------##
##-------------------------- Declaration des variables ----------------------##
##---------------------------------------------------------------------------##                

Pass=False                                          # permet de vérifier l'échec et mat
largeur_case=80                                     # doit correspondre a la taille des gif
bord=27
casier64=[]                                         # pour acceder une case sur les 64
casier=[]                                           # """"""""""" par ligne et colonne
casier_futur=[]                                     # pour avoir une idee du coup suivant
imagecase=[]        
imagecasesel=[] 
imagename=[]                                        # pour conserver l'indice de l'image
positionx=[]
positiony=[]
mouvements_possibles=[]                             # pour etudier les deplacements possibles.
couleurquijoue='Blanc'
caseselectionnee=False
caseselectionnee_x=0
caseselectionnee_y=0
grandrockblanc=True                                 # pour savoir si les rocks sont possibles
grandrocknoir=True                                  # --> (roi et tours non-déplacées)
rockblanc=True
rocknoir=True
mode_test=False
priseenpassant=False
position_pion_x=-4
position_pion_y=-4
liste_de_coups=[]
liste_echec=[]
pion_promotion_y=0
pion_promotion_x=0
validation_promotion=False

##---------------------------------------------------------------------------##
##--------------------------- Définition des Fonctions ----------------------##
##---------------------------------------------------------------------------##

#----------------------------- def deplace_piece(x,y) ------------------------#

def deplace_piece(x,y):                         # change dans le tableau casier[i][j], 
    global couleurquijoue                       # --> enlève dans l'ancienne case la piece
    global casier                               # --> et la met dans la nouvelle case
    global caseselectionnee_x 
    global grandrocknoir
    global grandrockblanc
    global rocknoir
    global rockblanc
    global priseenpassant,position_pion_x,position_pion_y
    global caseselectionnee_y
   
 # les 6 prochaines lignes sont la pour un historique potentiel et trace:
    lettres = "abcdefgh"
    espacenoir=''
    if couleurquijoue=="Noir": espacenoir='              '
    if  casier[x][y].piece=="Vide": symbole=' - '
    else: symbole=' X '+ casier[x][y].piece+" "
    print(espacenoir+casier[caseselectionnee_x][caseselectionnee_y].piece+" "\
          +lettres[caseselectionnee_x-1]\
          +str(caseselectionnee_y)+symbole+lettres[x-1]+str(y))
    
 # Prise en passant pour les pion:
    if priseenpassant and casier[caseselectionnee_x][caseselectionnee_y].piece=='Pion' \
       and caseselectionnee_x!=x and casier[x][y].piece=='Vide'\
    and mode_test==False:
 # On enleve mode test car condition pas assez restrictive
 # (pourrait faire disparaitre la pièce sans prise en passant)
            casier[position_pion_x][position_pion_y].piece='Vide'
            casier[position_pion_x][position_pion_y].habitee='Vide'
            l=trouve_index (position_pion_x,position_pion_y)
            dessin.create_image(casier[position_pion_x][position_pion_y].centrex, \
                                casier[position_pion_x][position_pion_y].centrey, \
                                image = imagecase[l])
            
    priseenpassant=False
    if casier[caseselectionnee_x][caseselectionnee_y].piece=='Pion' \
       and y-caseselectionnee_y==2 \
       or y-caseselectionnee_y==-2:
            priseenpassant=True
            position_pion_x=x
            position_pion_y=y
		
	
 # la nouvelle case recoit la piece
    casier[x][y].piece=casier[caseselectionnee_x][caseselectionnee_y].piece
    casier[x][y].habitee=casier[caseselectionnee_x][caseselectionnee_y].habitee
    casier[caseselectionnee_x][caseselectionnee_y].piece='Vide'
    casier[caseselectionnee_x][caseselectionnee_y].habitee='Vide' 
               
 # on remplace l'image de depart par la vide 
    l=trouve_index (caseselectionnee_x,caseselectionnee_y)
    dessin.create_image(casier[caseselectionnee_x][caseselectionnee_y].centrex, \
                        casier[caseselectionnee_x][caseselectionnee_y].centrey, \
                        image = imagecase[l])
    
 # on remplace l'image d'arrivee
    l=trouve_index (x,y)
    dessin.create_image(casier[x][y].centrex, casier[x][y].centrey, image = imagecase[l])

 # la fonction pour changer le pion
    pion_transformation(x,y)         

 #si on a pas un tour au coins de l'echiquier on annule le rock
 #si la tour peut être prise par une autre tour, """""" le rock
    
    if not(casier[1][1].piece)=='Tour' or casier[1][1].habitee=='Noir': grandrockblanc=False
    if not(casier[1][8].piece)=='Tour' or casier[1][8].habitee=='Blanc':grandrocknoir=False
    if not(casier[8][1].piece)=='Tour' or casier[8][1].habitee=='Noir': rockblanc=False 
    if not(casier[8][8].piece)=='Tour' or casier[8][8].habitee=='Blanc':rocknoir=False
    
    if not(casier[5][1].piece)=='Roi':
            rockblanc=False
            grandrockblanc=False
            
    if not(casier[5][8].piece)=='Roi':
            rocknoir=False
            grandrocknoir=False

    if casier[x][y].piece=='Roi':

            if couleurquijoue=='Blanc':     # le roi a bougé, donc pas de rock
                    grandrockblanc=False
                    rockblanc=False
            else:
                    grandrocknoir=False
                    rocknoir=False
                    
            if x-caseselectionnee_x==2 :    # deplacement de 2 donc rock! donc on rappelle la meme              
                   caseselectionnee_x=8     # -> fonction pour bouger tour! deja ete fait pour roi
                   deplace_piece(6,caseselectionnee_y)
                   
                   if couleurquijoue=='Blanc':couleurquijoue='Noir'
                   else: couleurquijoue='Blanc'
                   
            elif x-caseselectionnee_x==-2 : # deplacement de -2 donc grandrock
                   caseselectionnee_x=1
                   deplace_piece(4,caseselectionnee_y)
                   
                   if couleurquijoue=='Blanc':couleurquijoue='Noir' 
                   else: couleurquijoue='Blanc'
                   
    if couleurquijoue=='Blanc':couleurquijoue='Noir'
    else: couleurquijoue='Blanc'
    
    selectionne_piece(False)
    
    if couleurquijoue=="Blanc": message5.configure(bg="white")
    else:message5.configure(bg="black")

#----------------------- def bonne_piece(case_x,case_y) ----------------------#
        
def bonne_piece(case_x,case_y):         # on verifie que la case est une piece a jouer.  
    bonnepiece=False                    # -> pour l'instant on verifie que la piece
                                        # -> est de la bonne couleur, renvoie True or False
    
    if case_x >0 and case_y>0:          # si nous sommes sur les bords, afficher_case peut retourner (0,0)
            bonnepiece= (casier[case_x][case_y].habitee == couleurquijoue)
    return bonnepiece

#---------------------------- def charge_les_images --------------------------#

def charge_les_images ():               # charge les images en memoire dans un tableau 
    k=0                                 # -> avec un autre tableau qui pour le nom de l image, 
                                        # -> donne l'indice du tableau
    for i in range (1,9):    
        for j in range (1,9):
            existe=False
            nomimage = casier[i][j].piece+casier[i][j].habitee+casier[i][j].couleurfond+'.gif'
            nomimagesel = casier[i][j].piece+casier[i][j].habitee+casier[i][j].couleurfond+'Sel.gif'
            for k in range (0,len(imagename)):
                if imagename[k]==nomimage:
                    existe=True
            if not (existe):            
                imagecase.append( PhotoImage(file = nomimage))
                imagecasesel.append( PhotoImage(file = nomimagesel))
                imagename.append(nomimage)
            k=k+1

 # pour les pièces pas présentes sur l'échiquier
    imagecase.append( PhotoImage(file = 'ReineBlancNoir.gif')) 
    imagecasesel.append( PhotoImage(file = 'ReineBlancNoirSel.gif'))
    imagename.append('ReineBlancNoir.gif')
    imagecase.append( PhotoImage(file = 'ReineNoirBlanc.gif'))
    imagecasesel.append( PhotoImage(file = 'ReineNoirBlancSel.gif'))
    imagename.append('ReineNoirBlanc.gif')
    imagecase.append( PhotoImage(file = 'RoiNoirNoir.gif')) 
    imagecasesel.append( PhotoImage(file = 'RoiNoirNoirSel.gif'))
    imagename.append('RoiNoirNoir.gif')
    imagecase.append( PhotoImage(file = 'RoiBlancBlanc.gif'))
    imagecasesel.append( PhotoImage(file = 'RoiBlancBlancSel.gif'))
    imagename.append('RoiBlancBlanc.gif')

#--------------------------- def trouve_index (i,j) --------------------------#
    
def trouve_index (i,j):                 # va chercher l'index pour l'image de la case
        
    nomimage = casier[i][j].piece+casier[i][j].habitee+casier[i][j].couleurfond+'.gif'
    for indice in range (0,len(imagename)):
            if imagename[indice]==nomimage:
                    return indice
                
    return (0)             #au cas ou on ne trouve pas (pièces non présentes au début)

#------------------ def selectionne_piece (selectionne) ----------------------#

def selectionne_piece (selectionne):    # selectionne ou deselectionne la piece et repaint le canevas
        
        global caseselectionnee
        caseselectionnee= selectionne
        
        for i in range (1,9):
                for j in range (1,9):
                        if bonne_piece(i,j):
                            k=trouve_index(i,j)
                            if selectionne: 
 # on ne s'interresse qu'a enlever l'activeimage des pieces bonnes et on change l'image de la piece selectionnee.                                
                                if i==caseselectionnee_x and j==caseselectionnee_y:
                                        dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                            image = imagecasesel[k])
                                else:
                                        dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                            image = imagecase[k])
                            else: dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                      image = imagecase[k],activeimage = imagecasesel[k])

#-------------------------- def active_mode_test() ---------------------------#
                            
def active_mode_test():
    global mode_test
    mode_test=not(mode_test)
    
#-------------------------- def deplacement_valide(x,y) ----------------------#
    
def deplacement_valide(x,y):                                   # verifie si le deplacement peut se faire
        if casier[x][y].habitee==couleurquijoue : return False # on ne peut pas se deplacer sur ses propres pions
        else:
                for i in range (0,len(mouvements_possibles),2):
                       if x==mouvements_possibles[i] and y==mouvements_possibles[i+1]:return True
                return mode_test

#-------------------- def echec_si_mouvement(x,y,x1,y1) ----------------------#

def echec_si_mouvement(x,y,x1,y1): # a faire si la piece se deplace, y a t'il un echec? 
        global casier_futur        # --> verifier si le roi en etant un cav, un pion... peut atteindre une piece
        for i in range (1,9):
                for j in range (1,9):
                        casier_futur[i][j].piece=casier[i][j].piece
                        casier_futur[i][j].habitee=casier[i][j].habitee
        casier_futur[x1][y1].habitee=casier_futur[x][y].habitee
        casier_futur[x1][y1].piece=casier_futur[x][y].piece
        casier_futur[x][y].habitee="Vide"
        casier_futur[x][y].piece="Vide"
        print (x1)
        print (y1)
        print (casier_futur[x1][y1].piece)
        return mis_en_echec(couleurquijoue, casier_futur)

#--------------------- def mis_en_echec(couleur, casierx) ----------------------#

def mis_en_echec(couleur,casierx): # si le roi en etant cavalier, fou, tour et pion peut aller sur cette meme piece adverse, 
        print ('futur')            # --> alors c'est que cette piece adverse le met en echec!
        print (casier_futur[4][2].piece) #pour debug
        echec=False

 # peut annuler et remplace 6 lignes au dessus
        for i in range (1,9):
           for j in range (1,9):
                   if casierx[i][j].habitee==couleur:
                            if casierx[i][j].piece=='Roi':
                                x=i
                                y=j
        if couleur=='Blanc': autrecouleur='Noir'
        else : autrecouleur='Blanc'
        if couleur=='Blanc':
                if y<8:
                        if x<8: # verification de piece a prendre a droite
                                       if casierx[x+1][y+1].habitee=="Noir" \
                                          and casierx[x+1][y+1].piece=="Pion":
                                            echec= True
                        if x>1: # verification de piece a prendre a gauche
                                       if casierx[x-1][y+1].habitee=="Noir" \
                                          and casierx[x-1][y+1].piece=="Pion":
                                            echec= True               
        else:
                if y>1:
                        if x<8: # verification de piece a prendre a droite
                                       if casierx[x+1][y-1].habitee=="Blanc" \
                                          and casierx[x+1][y-1].piece=="Pion":
                                            echec= True
                        if x>1: # verification de piece a prendre a gauche
                                       if casierx[x-1][y-1].habitee=="Blanc" \
                                          and casierx[x-1][y-1].piece=="Pion":
                                            echec= True
                        # echec par Tour ou Reine
        k=x
        while k<8 and casierx[k+1][y].habitee=="Vide":k+=1
        if k<8 and(casierx[k+1][y].habitee==autrecouleur) \
           and (casierx[k+1][y].piece=="Tour" \
                or casierx[k+1][y].piece=="Reine"):echec= True
        k=x
        while k>1 and casier[k-1][y].habitee=="Vide":k-=1
        if k>1 and(casierx[k-1][y].habitee==autrecouleur) \
           and (casierx[k-1][y].piece=="Tour" \
                or casierx[k-1][y].piece=="Reine"):echec= True                
        k=y
        while k<8 and casierx[x][k+1].habitee=="Vide":k+=1
        if k<8 and(casierx[x][k+1].habitee==autrecouleur) \
           and (casierx[x][k+1].piece=="Tour" \
                or casierx[x][k+1].piece=="Reine"):echec= True
        k=y
        while k>1 and casierx[x][k-1].habitee=="Vide":k-=1
        if k>1 and(casierx[x][k-1].habitee==autrecouleur) \
           and (casierx[x][k-1].piece=="Tour" \
                or casierx[x][k-1].piece=="Reine"):echec= True
                         # echec par Fou ou Reine
        m=x
        n=y
        while m<8 and n<8 and casierx[m+1][n+1].habitee=="Vide":
                m+=1
                n+=1
        if m<8 and n<8 and (casierx[m+1][n+1].habitee==autrecouleur) \
           and (casierx[m+1][n+1].piece=="Fou" \
                or casierx[m+1][n+1].piece=="Reine"):echec= True
        m=x
        n=y
        while m<8 and n>1 and casierx[m+1][n-1].habitee=="Vide":
                m+=1
                n-=1
        if m<8 and n>1 and(casierx[m+1][n-1].habitee==autrecouleur) \
           and (casierx[m+1][n-1].piece=="Fou" \
                or casierx[m+1][n-1].piece=="Reine"):echec= True
        m=x
        n=y
        while m>1 and n>1 and casierx[m-1][n-1].habitee=="Vide":
                m-=1
                n-=1
        if m>1 and n>1 and(casierx[m-1][n-1].habitee==autrecouleur) \
           and (casierx[m-1][n-1].piece=="Fou" \
                or casierx[m-1][n-1].piece=="Reine"):echec= True
        m=x
        n=y
        while m>1 and n<8 and casierx[m-1][n+1].habitee=="Vide":
                m-=1
                n+=1
        if m>1 and n<8 and(casierx[m-1][n+1].habitee==autrecouleur) \
           and (casierx[m-1][n+1].piece=="Fou" \
                or casierx[m-1][n+1].piece=="Reine"):echec= True
                    # echec par Cavalier
        m=x
        n=y
        if m>2 and n>1:
                if (casierx[m-2][n-1].habitee==autrecouleur) \
                   and casierx[m-2][n-1].piece=="Cavalier":echec= True
        if m>2 and n<8:
                if (casierx[m-2][n+1].habitee==autrecouleur) \
                   and casierx[m-2][n+1].piece=="Cavalier":echec= True            
        if m<7 and n<8:
                if (casierx[m+2][n+1].habitee==autrecouleur) \
                   and casierx[m+2][n+1].piece=="Cavalier":echec= True
        if m<7 and n>1:
                if (casierx[m+2][n-1].habitee==autrecouleur) \
                   and casierx[m+2][n-1].piece=="Cavalier":echec= True
        if m>1 and n>2:
                if (casierx[m-1][n-2].habitee==autrecouleur) \
                   and casierx[m-1][n-2].piece=="Cavalier":echec= True
        if m>1 and n<7:
                if (casierx[m-1][n+2].habitee==autrecouleur) \
                   and casierx[m-1][n+2].piece=="Cavalier":echec= True
        if m<8 and n<7:
                if (casierx[m+1][n+2].habitee==autrecouleur) \
                   and casierx[m+1][n+2].piece=="Cavalier":echec= True
        if m<8 and n>2:
                if (casierx[m+1][n-2].habitee==autrecouleur) \
                   and casierx[m+1][n-2].piece=="Cavalier":echec= True
                
  # echec par roi (on sait que c'est interdit mais on ne doit pas avoir deux rois cote a cote)
        if x <8 and y<8:
                if (casierx[x+1][y+1].habitee==autrecouleur) \
                   and casierx[x+1][y+1].piece=="Roi":echec= True
        if y<8:
                if (casierx[x][y+1].habitee==autrecouleur) \
                   and casierx[x][y+1].piece=="Roi":echec= True
        if x> 1 and y<8:
                if (casierx[x-1][y+1].habitee==autrecouleur) \
                   and casierx[x-1][y+1].piece=="Roi":echec= True
        if x <8:
                if (casierx[x+1][y].habitee==autrecouleur) \
                   and casierx[x+1][y].piece=="Roi":echec= True  
        if x> 1:
                if (casierx[x-1][y].habitee==autrecouleur) \
                   and casierx[x-1][y].piece=="Roi":echec= True
        if x <8 and y>1:
                if (casierx[x+1][y-1].habitee==autrecouleur) \
                   and casierx[x+1][y-1].piece=="Roi":echec= True
        if y>1:
                if (casierx[x][y-1].habitee==autrecouleur) \
                   and casierx[x][y-1].piece=="Roi":echec= True
        if x> 1 and y>1:
                if (casierx[x-1][y-1].habitee==autrecouleur) \
                   and casierx[x-1][y-1].piece=="Roi":echec= True
        return echec

#------------------------- def calcule_mouvements(x,y) -------------------------#

def calcule_mouvements(x,y):                                                    # verifie quels sont les mouvements possibles.
    global mouvements_possibles,position_pion_x,position_pion_y
    global priseenpassant,liste_de_coups
    
    mouvements_possibles.clear()                                                # enleve les mouvements precedents
    liste_de_coups.clear()
    if casier[x][y].piece =='Pion':
            
            if couleurquijoue=='Blanc':
                    if y<8:
                            if casier[x][y+1].habitee=="Vide" \
                               and not (echec_si_mouvement(x,y,x,y+1)):
                                    mouvements_possibles.append(x)
                                    mouvements_possibles.append(y+1)
                                    if y==2 and casier[x][y+2].habitee=="Vide" \
                                       and not (echec_si_mouvement(x,y,x,y+2)): # si pion n'a jamais joué
                                            mouvements_possibles.append(x)
                                            mouvements_possibles.append(y+2)
                            if x<8: # verification de piece a prendre a droite
                                       if casier[x+1][y+1].habitee=="Noir" \
                                          and not (echec_si_mouvement(x,y,x+1,y+1)):
                                            mouvements_possibles.append(x+1)
                                            mouvements_possibles.append(y+1)
                                       elif priseenpassant and y==5 \
                                            and x==position_pion_x-1 \
                                            and not(echec_si_mouvement(x,y,+1,y+1)):
                                               mouvements_possibles.append(x+1)
                                               mouvements_possibles.append(y+1)
				      
                            if x>1: # verification de piece a prendre a gauche
                                       if casier[x-1][y+1].habitee=="Noir" \
                                          and not (echec_si_mouvement(x,y,x-1,y+1)):
                                            mouvements_possibles.append(x-1)
                                            mouvements_possibles.append(y+1)
                                            print("prise en passant")
                                       elif priseenpassant and y==position_pion_y \
                                            and x==position_pion_x+1 \
                                            and not(echec_si_mouvement(x,y,x-1,y+1)):
                                               mouvements_possibles.append(x-1)
                                               mouvements_possibles.append(y+1)
                                               print("prise en passant")
				        
            else:
                    if y>1:
                            if casier[x][y-1].habitee=="Vide" \
                               and not(echec_si_mouvement(x,y,x,y-1)):
                                    mouvements_possibles.append(x)
                                    mouvements_possibles.append(y-1)
                                    if y==7 and casier[x][y-2].habitee=="Vide" \
                                       and not(echec_si_mouvement(x,y,x,y-2)):   # si pion n a jamais joue
                                            mouvements_possibles.append(x)
                                            mouvements_possibles.append(y-2)
                            if x<8: # verification de piece a prendre a droite
                                       if casier[x+1][y-1].habitee=="Blanc" \
                                          and not(echec_si_mouvement(x,y,x+1,y-1)):
                                            mouvements_possibles.append(x+1)
                                            mouvements_possibles.append(y-1)
                                       elif priseenpassant and y==position_pion_y \
                                            and x==position_pion_x+1 \
                                            and not(echec_si_mouvement(x,y,x+1,y-1)):
                                               mouvements_possibles.append(x-1)
                                               mouvements_possibles.append(y-1)
                                               
                            if x>1: # verification de piece a prendre a gauche

                                       if casier[x-1][y-1].habitee=="Blanc" \
                                          and not(echec_si_mouvement(x,y,x-1,y-1)):
                                            mouvements_possibles.append(x-1)
                                            mouvements_possibles.append(y-1)
                                       elif priseenpassant and y==position_pion_y \
                                            and x==position_pion_x-1 \
                                            and not(echec_si_mouvement(x,y,x-1,y-1)):
                                               mouvements_possibles.append(x+1)
                                               mouvements_possibles.append(y-1)
                        
    elif casier[x][y].piece =='Tour':
            k=x
            while k<8 and not(casier[k+1][y].habitee==couleurquijoue):
                    liste_de_coups.append(k+1)
                    liste_de_coups.append(y)
                    print(mouvements_possibles)
 # ce changement permet de pouvoir attaquer une pièce a distance qui attaque le roi
                    if(echec_si_mouvement(x,y,k+1,y)): 
                            liste_de_coups.remove(k+1)
                            liste_de_coups.remove(y)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[k+1][y].habitee=="Vide"):break
                    k+=1
            k=x
            while k>1 and not(casier[k-1][y].habitee==couleurquijoue):
                    liste_de_coups.append(k-1)
                    liste_de_coups.append(y)
                    print("essai remonte3",mouvements_possibles)
                    if (echec_si_mouvement(x,y,k-1,y)):
                            liste_de_coups.remove(k-1)
                            liste_de_coups.remove(y)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[k-1][y].habitee=="Vide"):break
                    k-=1
            k=y
            while k>1 and not(casier[x][k-1].habitee==couleurquijoue):
                    liste_de_coups.append(x)
                    liste_de_coups.append(k-1)
                    if (echec_si_mouvement(x,y,x,k-1)):
                             liste_de_coups.remove(x)
                             liste_de_coups.remove(k-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                            
                    if not(casier[x][k-1].habitee=="Vide"):break
                    k-=1
            k=y
            while k<8 and not(casier[x][k+1].habitee==couleurquijoue):
                    liste_de_coups.append(x)
                    liste_de_coups.append(k+1)
                    if (echec_si_mouvement(x,y,x,k+1)):
                            liste_de_coups.remove(x)
                            liste_de_coups.remove(k+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[x][k+1].habitee=="Vide"):break
                    k+=1
                    
    elif casier[x][y].piece =='Cavalier':
            m=x
            n=y
            if m>2 and n>1:
                if not(casier[m-2][n-1].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m-2,n-1)):
                    mouvements_possibles.append(m-2)
                    mouvements_possibles.append(n-1)
            if m>2 and n<8:
                if not(casier[m-2][n+1].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m-2,n+1)):
                    mouvements_possibles.append(m-2)
                    mouvements_possibles.append(n+1)
            if m<7 and n<8:
                if not(casier[m+2][n+1].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m+2,n+1)):
                    mouvements_possibles.append(m+2)
                    mouvements_possibles.append(n+1)
            if m<7 and n>1:
                if not(casier[m+2][n-1].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m+2,n-1)):
                    mouvements_possibles.append(m+2)
                    mouvements_possibles.append(n-1)
            if m>1 and n>2:
                if not(casier[m-1][n-2].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m-1,n-2)):
                    mouvements_possibles.append(m-1)
                    mouvements_possibles.append(n-2)
            if m>1 and n<7:
                if not(casier[m-1][n+2].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m-1,n+2)):
                    mouvements_possibles.append(m-1)
                    mouvements_possibles.append(n+2)
            if m<8 and n<7:
                if not(casier[m+1][n+2].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m+1,n+2)):
                    mouvements_possibles.append(m+1)
                    mouvements_possibles.append(n+2)
            if m<8 and n>2:
                if not(casier[m+1][n-2].habitee==couleurquijoue)\
                   and not(echec_si_mouvement(x,y,m+1,n-2)):
                    mouvements_possibles.append(m+1)
                    mouvements_possibles.append(n-2)
                    
    elif casier[x][y].piece =='Fou':
            m=x
            n=y
            while m<8 and n<8 and not(casier[m+1][n+1].habitee==couleurquijoue):
                    liste_de_coups.append(m+1)
                    liste_de_coups.append(n+1)
                    if (echec_si_mouvement(x,y,m+1,n+1)):
                            liste_de_coups.remove(m+1)
                            liste_de_coups.remove(n+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m+1][n+1].habitee=="Vide"):break
                    m+=1
                    n+=1
            m=x
            n=y
            while m<8 and n>1 and not(casier[m+1][n-1].habitee==couleurquijoue):
                    liste_de_coups.append(m+1)
                    liste_de_coups.append(n-1)
                    if (echec_si_mouvement(x,y,m+1,n-1)):
                            liste_de_coups.remove(m+1)
                            liste_de_coups.remove(n-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m+1][n-1].habitee=="Vide"):break
                    m+=1
                    n-=1
            m=x
            n=y
            while m>1 and n<8 and not(casier[m-1][n+1].habitee==couleurquijoue):
                    liste_de_coups.append(m-1)
                    liste_de_coups.append(n+1)
                    if (echec_si_mouvement(x,y,m-1,n+1)):
                            liste_de_coups.remove(m-1)
                            liste_de_coups.remove(n+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m-1][n+1].habitee=="Vide"):break
                    m-=1
                    n+=1
            m=x
            n=y
            while m>1 and n>1 and not(casier[m-1][n-1].habitee==couleurquijoue):
                    liste_de_coups.append(m-1)
                    liste_de_coups.append(n-1)
                    if (echec_si_mouvement(x,y,m-1,n-1)):
                            liste_de_coups.remove(m-1)
                            liste_de_coups.remove(n-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m-1][n-1].habitee=="Vide"):break
                    m-=1
                    n-=1
                    
    elif casier[x][y].piece =='Reine':
            k=x
            while k<8 and not(casier[k+1][y].habitee==couleurquijoue):
                    liste_de_coups.append(k+1)
                    liste_de_coups.append(y)
                    print(mouvements_possibles)
 # ce changement permet de pouvoir attaquer une pièce a distance qui attaque le roi
                    if(echec_si_mouvement(x,y,k+1,y)):
                            liste_de_coups.remove(k+1)
                            liste_de_coups.remove(y)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[k+1][y].habitee=="Vide"):break
                    k+=1
            k=x
            while k>1 and not(casier[k-1][y].habitee==couleurquijoue):
                    liste_de_coups.append(k-1)
                    liste_de_coups.append(y)
                    print("essai remonte3",mouvements_possibles)
                    if (echec_si_mouvement(x,y,k-1,y)):
                            liste_de_coups.remove(k-1)
                            liste_de_coups.remove(y)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[k-1][y].habitee=="Vide"):break
                    k-=1
            k=y
            while k>1 and not(casier[x][k-1].habitee==couleurquijoue):
                    liste_de_coups.append(x)
                    liste_de_coups.append(k-1)
                    if (echec_si_mouvement(x,y,x,k-1)):
                             liste_de_coups.remove(x)
                             liste_de_coups.remove(k-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                            
                    if not(casier[x][k-1].habitee=="Vide"):break
                    k-=1
                    
            k=y
            while k<8 and not(casier[x][k+1].habitee==couleurquijoue):
                    liste_de_coups.append(x)
                    liste_de_coups.append(k+1)
                    if (echec_si_mouvement(x,y,x,k+1)):
                            liste_de_coups.remove(x)
                            liste_de_coups.remove(k+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[x][k+1].habitee=="Vide"):break
                    k+=1
            m=x
            n=y
            while m<8 and n<8 and not(casier[m+1][n+1].habitee==couleurquijoue):
                    liste_de_coups.append(m+1)
                    liste_de_coups.append(n+1)
                    if (echec_si_mouvement(x,y,m+1,n+1)):
                            liste_de_coups.remove(m+1)
                            liste_de_coups.remove(n+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m+1][n+1].habitee=="Vide"):break
                    m+=1
                    n+=1
            m=x
            n=y
            while m<8 and n>1 and not(casier[m+1][n-1].habitee==couleurquijoue):
                    liste_de_coups.append(m+1)
                    liste_de_coups.append(n-1)
                    if (echec_si_mouvement(x,y,m+1,n-1)):
                            liste_de_coups.remove(m+1)
                            liste_de_coups.remove(n-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m+1][n-1].habitee=="Vide"):break
                    m+=1
                    n-=1
            m=x
            n=y
            while m>1 and n<8 and not(casier[m-1][n+1].habitee==couleurquijoue):
                    liste_de_coups.append(m-1)
                    liste_de_coups.append(n+1)
                    if (echec_si_mouvement(x,y,m-1,n+1)):
                            liste_de_coups.remove(m-1)
                            liste_de_coups.remove(n+1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m-1][n+1].habitee=="Vide"):break
                    m-=1
                    n+=1
            m=x
            n=y
            while m>1 and n>1 and not(casier[m-1][n-1].habitee==couleurquijoue):
                    liste_de_coups.append(m-1)
                    liste_de_coups.append(n-1)
                    if (echec_si_mouvement(x,y,m-1,n-1)):
                            liste_de_coups.remove(m-1)
                            liste_de_coups.remove(n-1)
                    mouvements_possibles.extend(liste_de_coups)
                    liste_de_coups.clear()
                    if not(casier[m-1][n-1].habitee=="Vide"):break
                    m-=1
                    n-=1
           
    elif casier[x][y].piece =='Roi':
                if y<8:
                        if not(casier[x][y+1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x,y+1)):
                                    mouvements_possibles.append(x)
                                    mouvements_possibles.append(y+1)
                        if x<8 and not(casier[x+1][y+1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x+1,y+1)):
                                    mouvements_possibles.append(x+1)
                                    mouvements_possibles.append(y+1)
                        if x>1 and not(casier[x-1][y+1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x-1,y+1)):
                                    mouvements_possibles.append(x-1)
                                    mouvements_possibles.append(y+1)
                                    print (x-1)
                                    print (y+1)
                if y>1:
                        if not(casier[x][y-1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x,y-1)):
                                    mouvements_possibles.append(x)
                                    mouvements_possibles.append(y-1)
                        if x<8 and not(casier[x+1][y-1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x+1,y-1)):
                                    mouvements_possibles.append(x+1)
                                    mouvements_possibles.append(y-1)
                        if x>1 and not(casier[x-1][y-1].habitee==couleurquijoue) \
                           and not(echec_si_mouvement(x,y,x-1,y-1)):
                                    mouvements_possibles.append(x-1)
                                    mouvements_possibles.append(y-1)
                
                if x>1 and casier[x-1][y].habitee=="Vide" and not(echec_si_mouvement(x,y,x-1,y)):
                                    mouvements_possibles.append(x-1)
                                    mouvements_possibles.append(y)
                                    # grand rock
                                    if couleurquijoue=="Blanc":
                                            if grandrockblanc and casier[3][y].habitee=="Vide" \
                                               and casier[2][y].habitee=="Vide" \
                                               and not(echec_si_mouvement(x,y,x-2,y)): # on est forcement en X=5
                                                    mouvements_possibles.append(x-2)
                                                    mouvements_possibles.append(y)
                                    else:
                                            if grandrocknoir and casier[3][y].habitee=="Vide" \
                                               and casier[2][y].habitee=="Vide" \
                                               and not(echec_si_mouvement(x,y,x-2,y)): # on est forcement en X=5
                                                    mouvements_possibles.append(x-2)
                                                    mouvements_possibles.append(y)
                                    
                if x<8 and casier[x+1][y].habitee=="Vide" and not(echec_si_mouvement(x,y,x+1,y)):
                                    mouvements_possibles.append(x+1)
                                    mouvements_possibles.append(y)
                                    # petit rock
                                    if couleurquijoue=="Blanc":
                                            if rockblanc and casier[7][y].habitee=="Vide" \
                                               and not(echec_si_mouvement(x,y,x+2,y)): # on est forcement en X=5 et on vient d etudier X=6
                                                    mouvements_possibles.append(x+2)
                                                    mouvements_possibles.append(y)
                                    else:
                                            if rocknoir and casier[7][y].habitee=="Vide"  \
                                               and not(echec_si_mouvement(x,y,x+2,y)): # on est forcement en X=5
                                                    mouvements_possibles.append(x+2)
                                                    mouvements_possibles.append(y)


#---------------------- def marque_case_possibles(marque) ----------------------#
                                                    
def marque_case_possibles(marque):                                                  # si marque afficher un petit rouge sur le coin de la case, sinon enlever la marque
    global casier

 # definie le centre de haut gauche de la case et met la couleur
    for i in range (0,len(mouvements_possibles),2):
        x=mouvements_possibles[i]
        y=mouvements_possibles[i+1]
        if marque:
                dessin.create_image(casier[x][y].centrex-32, casier[x][y].centrey-32, image = Coinrouge)
        elif casier[x][y].couleurfond=="Blanc":
                dessin.create_image(casier[x][y].centrex-32, casier[x][y].centrey-32, image = Coinblanc)
        else:
                dessin.create_image(casier[x][y].centrex-32, casier[x][y].centrey-32, image = Coinnoir)
        
#------------------------ def afficher_case(event) -----------------------------#
                
def afficher_case(event):                                                            # Fonction basée sur un exercice, lorsqu'on clique sur
    global caseselectionnee                                                          # -> l'image activee, donne les coordonnes de la case
    global caseselectionnee_x
    global caseselectionnee_y
    global validation_promotion
    
    if validation_promotion:
            casier[pion_promotion_x][pion_promotion_y].piece=promotion.get()
            z=trouve_index(pion_promotion_x,pion_promotion_y)
            dessin.create_image(casier[pion_promotion_x][pion_promotion_y].centrex, \
                                casier[pion_promotion_x][pion_promotion_y].centrey, image = imagecase[z])
            validation_promotion=False
            
    abscisse = event.x
    ordonnee = event.y
    indexx='z'
    indexy=0
    case_x=0
    case_y=0
    message3.configure(text="")

    for i in range (1,9):
        if abscisse >=positionx[i].minimum:
            if abscisse <positionx[i].maximum:
                indexx=positionx[i].indexlettre
                case_x=positionx[i].index
    for j in range (1,9):
        if ordonnee >=positiony[j].minimum:
            if ordonnee <positiony[j].maximum:
                case_y=positiony[j].index
                
    if caseselectionnee:
        if case_x==caseselectionnee_x and case_y==caseselectionnee_y: 
            selectionne_piece (False)
            marque_case_possibles(False)
            message.configure(text="case selectionnee: aucune")
        else:
            if deplacement_valide(case_x,case_y):
                    caseselectionnee= False
                    marque_case_possibles(False)
                    deplace_piece(case_x,case_y)                    
                    if mis_en_echec(couleurquijoue,casier):
                            message2.configure(text="Echec")
                            if echec_et_mat(couleurquijoue):
                                    message2.configure(text="Echec et mat!!!")
                    else: message2.configure(text="")
            else:
                    message3.configure(text="deplacement non Valide!")
            
    else:
 #on verifie que la case est une piece a jouer. pour l instant on verifie simplement que la piece est de la bonne couleur.
        if bonne_piece(case_x,case_y):
                caseselectionnee_x=case_x
                caseselectionnee_y=case_y
                calcule_mouvements(case_x,case_y)
                message.configure(text="case selectionnee: "+ indexx +str(caseselectionnee_y))
                marque_case_possibles(True)
                selectionne_piece (True)
        
#---------------------------- def initialisation() -----------------------------#
                
def initialisation ():
    k=0
    FondBlanc=False
    casier64.append(Cases())
    positionx.append(Positions())
    positiony.append(Positions())
    lettres='abcdefghij'
    for i in range (1,10):
            casier.append([0,0,0,0,0,0,0,0,0])                                 # initialisation du tableau
            casier_futur.append([0,0,0,0,0,0,0,0,0])
            positionx.append(Positions())
            positionx[i].minimum=largeur_case*(i-1)+bord
            positionx[i].maximum=largeur_case*(i)+bord
            positionx[i].indexlettre=lettres[i-1]                              # commence a 0
            positionx[i].index=i

    for j in range (1,9):
            positiony.append(Positions())
            positiony[j].maximum=694-(largeur_case*(j-1)+bord)
            positiony[j].minimum=694-(largeur_case*(j)+bord)
            positiony[j].index=j
            
    for i in range (1,9):
        for j in range (1,9):
            k=k+1
            casier[i][j]=Cases()                                               # besoin de creer chaque fois une nouvelle 
            casier_futur[i][j]=Cases()                                         # -> instance car sinon casex est la meme.
            casier[i][j].colonne=j
            casier[i][j].ligne=i
            casier[i][j].centrex=largeur_case*(i-1)+largeur_case/2+bord
            casier[i][j].centrey=694-(largeur_case*(j-1)+largeur_case/2+bord)  #pour partir du bas 
            casier[i][j].habitee="Vide"
            casier_futur[i][j].habitee="Vide"
            casier[i][j].piece='Vide'
            casier_futur[i][j].piece='Vide'
            if FondBlanc:
                casier[i][j].couleurfond="Blanc"
            else:
                casier[i][j].couleurfond="Noir" 
            FondBlanc= not FondBlanc
        FondBlanc= not FondBlanc
    for i in range (1,9):
        casier[i][2].piece='Pion'
        casier[i][7].piece='Pion'
        casier_futur[i][2].piece='Pion'
        casier_futur[i][7].piece='Pion'
        for j in range(1,3):
            casier[i][j].habitee='Blanc'
            casier_futur[i][j].habitee='Blanc'
        for j in range(7,9):
            casier[i][j].habitee='Noir'
            casier_futur[i][j].habitee='Noir'

    casier[1][1].piece='Tour'
    casier[1][8].piece='Tour'
    casier[8][1].piece='Tour'
    casier[8][8].piece='Tour'
    casier_futur[1][1].piece='Tour'
    casier_futur[1][8].piece='Tour'
    casier_futur[8][1].piece='Tour'
    casier_futur[8][8].piece='Tour'

    casier[2][1].piece='Cavalier'
    casier[7][1].piece='Cavalier'
    casier[2][8].piece='Cavalier'
    casier[7][8].piece='Cavalier'
    casier_futur[2][1].piece='Cavalier'
    casier_futur[7][1].piece='Cavalier'
    casier_futur[2][8].piece='Cavalier'
    casier_futur[7][8].piece='Cavalier'

    casier[3][1].piece='Fou'
    casier[6][1].piece='Fou'
    casier[3][8].piece='Fou'
    casier[6][8].piece='Fou'
    casier_futur[3][1].piece='Fou'
    casier_futur[6][1].piece='Fou'
    casier_futur[3][8].piece='Fou'
    casier_futur[6][8].piece='Fou'
    
    casier[4][1].piece='Reine'
    casier[4][8].piece='Reine'
    casier_futur[4][1].piece='Reine'
    casier_futur[4][8].piece='Reine'
    
    casier[5][1].piece='Roi'
    casier[5][8].piece='Roi'
    casier_futur[5][1].piece='Roi'
    casier_futur[5][8].piece='Roi'
    m=casier

#---------------------------- def dessiner_lechiquier() ----------------------------#

def dessiner_lechiquier ():
    message5.configure(bg="white")
    for i in range (1,9):
        for j in range (1,9):            
            nomimage = casier[i][j].piece+casier[i][j].habitee+casier[i][j].couleurfond+'.gif'
            for k in range (0,len(imagename)):
                if imagename[k]==nomimage:
                    if couleurquijoue==casier[i][j].habitee :                                   # verification de la couleur qui joue pour activer activeimage
                        if caseselectionnee:
                            print ('on est select')
                            if i==caseselectionnee_x and j==caseselectionnee_y:
                                dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                    image = imagecasesel[k],activeimage = imagecasesel[k])
                            else:
                                dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                    image = imagecase[k])
                        else:
                            dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                                image = imagecase[k],activeimage = imagecasesel[k])
                    else:
                       dessin.create_image(casier[i][j].centrex, casier[i][j].centrey, \
                                           image = imagecase[k])

#------------------------------ def f_pion_promotion() -----------------------------#
                       
def f_pion_promotion():
        fenetre_pion= Toplevel()
        fenetre_pion.title("Pion Promotion")
        fenetre_pion.geometry("300x150+20+120")
        nom_piece= ['Reine   ', 'Tour    ', 'Fou     ','Cavalier']
        nom_piecev= ['Reine', 'Tour', 'Fou','Cavalier']                                         # deux liste permet d'éviter les espaces et de donnés les bonnes valeurs
        for i in range(4):
                a = Radiobutton(fenetre_pion, variable=promotion, text=nom_piece[i], \
                                value=nom_piecev[i])
                a.pack()                                                                        # boucle créant les bouton radios
        button_ok=Button(fenetre_pion, text='Ok', command =fenetre_pion.destroy, \
                         background="white")
        button_ok.pack(ipadx=50,ipady=0)
        button_Valider=Button(fenetre_pion, text='Valider', command =valider_promotion, \
                              background="#0A4C86",activebackground="green")
        button_Valider.pack(ipadx=50,ipady=0)

#------------------------ def pion_transformation(x,y) -------------------------#
        
def pion_transformation(x,y):
        global validation_promotion,pion_promotion_x,pion_promotion_y
        if casier[x][y].piece=='Pion' and (y==1 or  y==8):
                f_pion_promotion()
                validation_promotion=True
                pion_promotion_x=x
                pion_promotion_y=y
                
#------------------------ def echec_et_mat(couleur) ----------------------------#
                
def echec_et_mat(couleur):                                                                      # appele de la fonctiion dans afficher_case
        global liste_echec                                                                      # vérifie si le mouvement des pièce est encore possible
        for j in range(1,9):
                for i in range(1,9):
                        if casier[i][j].habitee==couleur:
                                calcule_mouvements(i,j)
                                liste_echec.extend(mouvements_possibles)
        if liste_echec==[]:
                echecetmat=True
                echec = Toplevel(fen)
                echec.title("Echec!")
                echec.geometry("300x150+20+120")
                nom_choix= ['Quitter   ', 'Recommencer']
                nom_choixv= ['Quitter', 'Recommencer']                                             
                for i in range(2):
                    a = Radiobutton(echec, variable=promotion, \
                                    text=nom_choix[i], value=nom_choixv[i])
                    a.pack()                                                                                                  
                button_quitter=Button(echec, text='Quitter', \
                                      command =fen.destroy,background="white")
                button_quitter.pack(ipadx=50,ipady=0)
                button_recommencer=Button(echec, text='Recommencer',\
                                          activebackground="green")
                button_recommencer.pack(ipadx=50,ipady=0)

        else:
                echecetmat=False
        liste_echec.clear()
        return echecetmat

#---------------------------- def valider_promotion() ---------------------------#

def valider_promotion():
        global casier
        casier[pion_promotion_x][pion_promotion_y].piece=promotion.get()
        z=trouve_index(pion_promotion_x,pion_promotion_y)
        dessin.create_image(casier[pion_promotion_x][pion_promotion_y].centrex, \
                            casier[pion_promotion_x][pion_promotion_y].centrey, image = imagecase[z])

#---------------------------------- def reload() --------------------------------#
        
def reload():
        global Pass,couleurquijoue
        Pass=False
        couleurquijoue='Blanc'
        caseselectionnee=False
        caseselectionnee_x=0
        caseselectionnee_y=0
        grandrockblanc=True  # pour savoir si les rocks sont possibles (roi et tours non deplaces)
        grandrocknoir=True
        rockblanc=True
        rocknoir=True
        mode_test=False
        priseenpassant=False
        position_pion_x=-4
        position_pion_y=-4
        validation_promotion=False

##---------------------------------------------------------------------------##
##--------------------------- Création de la fenêtre ------------------------##
##---------------------------------------------------------------------------##
        
fen = Tk()
fen.title("Jeux d'Echec")

##---------------------------------------------------------------------------##
##----------------------------- Zones de texte ------------------------------##
##---------------------------------------------------------------------------##

message = Label(fen, text="Vous avez selectionné:")
message.grid(row = 1, column = 2, columnspan = 1, padx = 3, pady = 3, sticky = W+E)
message1 = Label(fen, text="Joueur:")
message1.grid(row = 1, column = 0, columnspan = 1, padx = 3, pady = 3, sticky = W+E)
message2 = Label(fen, text="",fg="green")
message2.grid(row = 2, column = 0, columnspan = 1, padx = 3, pady = 3, sticky = W+E)
message3 = Label(fen, text="",fg="red")
message3.grid(row = 1, column = 3, columnspan = 2, padx = 3, pady = 3, sticky = W+E)
message5 = Label(fen, text="    ",bg="white")
message5.grid(row = 1, column = 1, columnspan = 1, padx = 3, pady = 3, sticky = W+E)
"""certain des labels ne seront pas afficher car problème de résolution pour l'ordinateur de adam qui
a était obliger de mettre les boutons en haut ce qui cache les lables.Mais les lables essentielle sont là"""

##---------------------------------------------------------------------------##
##------------------------------- Boutons -----------------------------------##
##---------------------------------------------------------------------------##

bouton_quitter = Button(fen, text='Quitter', command = fen.destroy)                             # Bouton Quitter
bouton_quitter.grid(row = 1, column = 0, columnspan = 2,padx = 3, pady = 3, sticky = S+W+E)
bouton_test = Button(fen, text='mode test',command=active_mode_test,background="#AA0113")       # Bouton Recommencer (vide pour l'instant)
bouton_test.grid(row = 1, column = 2, padx = 3, pady = 3, sticky = S+W+E)
promotion= StringVar()
promotion.set("Reine")


##---------------------------------------------------------------------------##
##-------------------------------- Canevas ----------------------------------##
##---------------------------------------------------------------------------##

dessin = Canvas(fen, bg ="white", width = 800, height = 694)
dessin.grid(row =2, column = 2, columnspan = 3, padx =2, pady = 2, sticky = S+W+E)
Bord= PhotoImage(file = 'Bords.gif', master = dessin)
Coinrouge=PhotoImage(file = 'coinrouge.gif', master = dessin)                                   # pour marquer une case comme deplacement possible
Coinblanc=PhotoImage(file = 'coinblanc.gif', master = dessin)                                   # pour enlever la marque si case blanche
Coinnoir=PhotoImage(file = 'coinnoir.gif', master = dessin)                                     # pour enlever la marque si case noire
dessin.create_image(347, 347, image = Bord)

##---------------------------------------------------------------------------##
##-------------------------- Programme principal ----------------------------##
##---------------------------------------------------------------------------##

initialisation()
charge_les_images()
dessiner_lechiquier()
dessin.bind('<Button-1>', afficher_case)                                                       # Pour les coordonnées des cases                                                                  
fen.mainloop()                                                                                 # Boucle d'attente des événements (obligatoire)

##############################################################################################################################################################

