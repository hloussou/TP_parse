#https://www.dcode.fr/code-ascii

from asyncore import read
from distutils.log import error
import sys
import re


T_H =9 #taille bloc H
type_bloc=0
lbloc=0

def lecture_bloc(tab):
    tab_lbloc=[0,0,0,0]
    lbloc=0
    type_bloc=tab[0] #+ 1 type bloc
    tab.pop(0)
    for i in range (4): #+ 4 longeur de bloc
        tab_lbloc[i]=tab[0] 
        tab.pop(0)
    lbloc=tab_lbloc[3]+tab_lbloc[2]*10+tab_lbloc[1]*100+tab_lbloc[0]*1000
    
    ##print("Type de bloc :")
    ##print(chr(type_bloc))
    ##print("Longueur du bloc :")
    ##print(lbloc)    
    return tab, type_bloc,lbloc

def bloc_H (tab,tab_blocH):
    tab_blocH=[0]*T_H
    for i in range (len(tab_blocH)): #récupération des éléments du bloc H
        tab_blocH[i]=tab[0]
        tab.pop(0)
    return tab, tab_blocH

def bloc_C(tab,l,tab_blocC):
    for i in range (l): #récupération des éléments du bloc C
        tab_blocC.append(tab[0])
        tab.pop(0)
    return tab, tab_blocC

def bloc_D(tab,l,tab_blocD):
    for i in range (l): #récupération des éléments du bloc D
        tab_blocD.append(tab[0])
        tab.pop(0)
    return tab, tab_blocD
   

def read_blocH(tab_blocH): #lecture du bloc H
    largeur=tab_blocH[3]+tab_blocH[2]*10+tab_blocH[1]*100+tab_blocH[0]*1000 #calcul largeur
    hauteur=tab_blocH[7]+tab_blocH[6]*10+tab_blocH[5]*100+tab_blocH[4]*1000 #calcul hauteur
    type_pixel=tab_blocH[8]
    print("Largeur :", largeur)
    print("Hauteur :", hauteur)
    print("Type de pixel : ", type_pixel)
    print("")
    return largeur

def read_blocC(tab_blocC): #lecture du bloc C
    print("Commentaires : ")
    for j in range (len(tab_blocC)): 
        print(chr(tab_blocC[j]),end=''); #affichage du commentaire sur une ligne
    print("")


def read_blocD(tab_blocD,largeur): #lecture du bloc D
    for j in range (len(tab_blocD)):
        m=0;
        t=bin(tab_blocD[j]).lstrip('-0b') #converti en binaire chaque 'int' du block D
        scale=(len(t)-8)*-1 #différence du nombre de bit entre la largeur de l'image et le 'int' du block
        print("")
        tab=[0]*len(t)
        for l in range (len(t)): #on mets les données dans un tableau
            tab[l]=t[l]
        while(scale>0): # on ajoute le nombre de 0 pour avoir une taille de 8 
            tab.insert(0,"0")
            scale-=1  
        for k in range (len(tab)):
            if(m==largeur): # si on dépasse la largeur de l'image : retour à la ligne
                print("");
            if (tab[k]=="0"):
                print("X", end='') #Si bit 0 on affiche une croix
            if (tab[k]=="1"):
                print(" ", end='')
            m+=1
    print("")
    
def check(path): #vérification qu'on rentre pas n'importe quoi en paramètre, exemple valide : ./A.mp
    if path.isspace(): #pas d'espace autorisé
        return False
    else:
        if re.search("\.mp$", path): #doit finir par .mp
            return True
        else: 
            return False
        


if __name__ == '__main__':
    path = sys.argv[1]; #on récupére le chemin d'accès
    if(check(path)):#vérification de l'argument 
        try:
            f = open(path,'rb') # opening a binary file
        except:
            print("Fichier non valide")
        content = f.read();
        tab_marqueur=[0]*8 #initialisation
        tab_suite=[]
        largeur=0
        tab_blocH=[]
        tab_blocC=[]
        tab_blocD=[]
        for octet in content : # On récupérer tous les éléments dans tab_suite
            tab_suite.append(octet)
        for i in range (8) : #8 octets "Mini-PNG"  
            tab_marqueur[i]=tab_suite[0]
            tab_suite.pop(0)
        print("Nom du marqueur : ")
        for j in range (len(tab_marqueur)):
            print(chr(tab_marqueur[j]),end='');
        print("")
        while(len(tab_suite)>1): #Tant que tab_suite n'est pas vide, on récupére des blocs
            tab_suite, type_bloc, lbloc = lecture_bloc(tab_suite)
            if (chr(type_bloc)=="H"): #Si c'est un type H
                tab_suite, tab_blocH = bloc_H(tab_suite,tab_blocH)
            elif (chr(type_bloc)=="C"): #Si c'est un type C
                tab_suite, tab_blocC = bloc_C(tab_suite,lbloc,tab_blocC)
            elif (chr(type_bloc)=="D"):#Si c'est un type D
                tab_suite,tab_blocD = bloc_D(tab_suite,lbloc,tab_blocD)
            else :
                print("Type de bloc non reconnu ")
                break;
        largeur = read_blocH(tab_blocH); #Ensuite on lis les blocs
        read_blocC(tab_blocC);
        read_blocD(tab_blocD,largeur);
    else :
        print("Nom du fichier non valide")