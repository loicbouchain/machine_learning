import random as rand
import networkx as nx
import matplotlib.pyplot
import time
import numpy as np

NB_NODE_MAX=100
CENTRALISATION_MAX=(NB_NODE_MAX/2)
NB_LONG_MAX=100
nb_fourmi = 500
nb_essai = 5
villeEnCours=""
ville_fin=19
G=nx.Graph()
shortestpath=[]
path=[]
def init():
    for x in range(NB_NODE_MAX):
        G.add_edge(rand.randrange(0, CENTRALISATION_MAX), rand.randrange(0, CENTRALISATION_MAX), longueur=rand.randrange(1, NB_LONG_MAX), pheromone=1)
    


def choisirVilleSuivante(index,villevisite):#permet de choisir la ville suivante aléatoirement mais en fonction des phéromones
    ville = index
    arrayVoisins=[]
    arrayVoisins.append(index)
    pourcentageChoix={}
    #pheromone level * (1/longueur)  / somme de pheromone level*1/longueur du chemin 1 , 2 ,3 .....
    if G.degree[index]>0:
        voisins = G[index]
        for voisin in voisins : 
            arrayVoisins.append(voisin)

            if voisin in villevisite:
                pourcentageChoix[voisin]=((100/len(voisins))+(G[index][voisin]["pheromone"] * (1/LongueurTotal()) )/ (PheromoneTotal()*(1/G[index][voisin]["longueur"])))/4 #une ville deja visité a moins de chance d'être choisi, le but est de parcourir le maximum de chemin pour trouver le plus court
            else :
                pourcentageChoix[voisin]=(100/len(voisins))+(G[index][voisin]["pheromone"] * (1/LongueurTotal()) )/ (PheromoneTotal()*(1/G[index][voisin]["longueur"]))#une ville non visité a plus de chance d'être choisi
                #print(pourcentageChoix)
            ville = RandomVoisin(pourcentageChoix) 
            if str(voisin) == str(ville_fin) :
     
                ville = ville_fin

    path.append(ville)
    #print(ville)
    return ville
        

    
def RandomVoisin(pourcentageChoix): #choix aléatoire du voisin
    choix = []
    for voisin in pourcentageChoix: 
        for i in range(int(pourcentageChoix[voisin])): #On créé une liste avec des voisins, chaque voisin est ajouté le nombre de fois défini par pourcentageChoix ainsi une liste de choix prendra la forme [72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 243, 243, 243, 243, 243, 243, 243, 243, 243, 243, 382, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41]
            choix.append(voisin)
    return choix[rand.randrange(0,len(choix))] #on prend un élément au hasard dans la liste choix 


def DeposerPheromone(path): # dépose des phéromones

    for x in range(0, len(path)):
        if x+1 != len(path) :
            G.edges[path[x],path[x+1]]["pheromone"] = G.edges[path[x],path[x+1]]["pheromone"] +50+1/LongueurPath(path) #on ajoute un nombre de phéromone plus ou moins grand en fonction de la longueur du chemin pour définir les chemin plus court comme meilleur


def EvaporationPheromone():#évaporation de 20% des phéromones 
    for chemin in G.edges():
        G.edges[chemin]["pheromone"] = G.edges[chemin]["pheromone"]*0.8

def LongueurPath(path):#défini la longueur du chemin
    longueurTotal=0
    if len(path) == 0 : 
        longueurTotal=9999999999
    
    for x in range(0, len(path)):
        if x+1 != len(path) :
           longueurTotal= longueurTotal+ G.edges[path[x],path[x+1]]["longueur"] 
    return longueurTotal

def LongueurTotal(): #défini la longueur totale 
    longueur = 0 
    for chemin in G.edges():
        longueur= longueur+G.edges[chemin]["longueur"]
    return longueur

def PheromoneTotal():#défini le nombre de phéromones total
    pheromone = 0 
    for chemin in G.edges():
        pheromone= pheromone+G.edges[chemin]["pheromone"]
    return pheromone

if __name__ == "__main__":
    init()
    
    shortestpath=[]
    plusPetitChemin=[]
    arrayGraphglobal=[]
    graphDistance = matplotlib.pyplot 
    print("Début du programme")
    for x in range(0,nb_essai):#pour un nombre d'essai donné
        print("Essai numéro : "+str(x))
        villeEnCours=0
        path.clear()
        shortestpath.clear()
        path.append(villeEnCours)
        villevisite=[0]
        arraygraph=[]
        for i in range(0,nb_fourmi):
            print("Fourmi n° : "+str(i))
            villeEnCours=0
            path=[]
            path.append(villeEnCours)
            while (ville_fin != villeEnCours):
                villeEnCours = choisirVilleSuivante(villeEnCours,villevisite)#choix d'une nouvelle ville
                villevisite.append(villeEnCours)
            DeposerPheromone(path) #dépose phéromone
            if LongueurPath(path) < LongueurPath(shortestpath):
                shortestpath = path#défini le chemin le plus cours rencontré
            arraygraph.append(LongueurPath(path))
        EvaporationPheromone()
        arrayGraphglobal.append(np.mean(arraygraph)) #moyenne des chemins
        print("Chemin le plus court de cet essai "+str(LongueurPath(shortestpath))+" mètres")
        print(shortestpath)

        if LongueurPath(shortestpath) < LongueurPath(plusPetitChemin):
            plusPetitChemin = shortestpath
    print("Chemin le plus court de tout les essais "+str(LongueurPath(plusPetitChemin))+" mètres")
    print(plusPetitChemin)
    graphDistance.plot(arrayGraphglobal)
    graphDistance.ylabel('Distance en mètre')
    graphDistance.show()
 

"""
    calculer longueur du chemin que la fourmi a prit 
    mettre 1/longueur total Pheromone par lien passé  
    evaporation = 0.5* pheromone calcul si on passe pas de dessus
    proba de choisir lien = pheromone level * (1/longueur)  / somme de pheromone level*1/longueur du chemin 1 , 2 ,3 .....
    https://www.youtube.com/watch?v=783ZtAF4j5g&t=663s
"""
