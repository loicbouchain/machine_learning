import random as rand
from math import *
import matplotlib.pyplot 
import numpy as np

indexChange=[]
pesanteur = 9.81
NUMBER_OF_SCORPION = 5000
DISTANCE_SHOOT_FITNESS =30

DISTANCE_SHOOT_CONDITION=300
FITNESS_SCORE_CONDITION=16000
arrayDistance=[]
class Scorpion:

    def __init__(self):
        self.lb = rand.uniform(1, 10)# longueur bras arc
        self.b = rand.uniform(1, 3)# base de la section arc
        self.h = rand.uniform(0.1, 0.5)# hauteur de la section du bras arc
        self.lc = rand.uniform(0.5, 10)# longueur corde
        self.lf = rand.uniform(0.1, 10)# longueur fleche
        self.a = rand.randrange(1, 180) #angle alpha
        self.p = rand.uniform(0.1, 1) #masse volumique fleche pour bois
        self.bf = rand.uniform(1, 100)# base section fleche
        self.hf = rand.uniform(1, 100)#hauteur section fleche
        self.df = rand.uniform(1, 50)#dimatere fleche
        self.youngmodule = rand.randrange(1, 100) # module de young du bois
        self.coeffpoisson = 0.2 #coeff poisson bois
        self.fitness = 0
        self.d =0
        self.isTire = True
        self.isRupture = False
        

def  ressortK(young, coeffpoisson):
    return 1/3* (young/(1-2*coeffpoisson))

def longueurAVide(lb,lc):
    if lb > lc :
        return 0.5*(sqrt((lb**2)-(lc**2)))
    else : 
        return 0

def longueurDeplacement(lf,lv):
    return lf-lv

def masseProjectile(p,b,h,lf):
    return p*b*h*lf

def velocite(ressortK,longueurDeplacement,masseProjectile):
    return sqrt((ressortK*(longueurDeplacement**2))/(masseProjectile))

def portee(velocite,pesanteur,a):
    return velocite**2/pesanteur*sin(2 * radians(a))

def energieImpact(masseProjectile,velocite):
    return 0.5*masseProjectile*(velocite**2)

def energieTnt(energieImpact):
    return energieImpact/4184

def is_rupture(longueurDeplacement,b,h,ressortK,lb,youngmodule):
    i = (b*(h**3))/12
    force_traction = ressortK * longueurDeplacement
    f = (force_traction*(lb**3))/(48*youngmodule*i)

    if longueurDeplacement>f:
        return True
    else:
        return False

def is_tire(longueurAVide,longueurFleche,longueurCorde,longueurArc): #retourne vrai si le scorpion peut tirer
    res = True
    if longueurAVide>longueurFleche:
        res=False
    
    if longueurCorde>longueurArc:
        res=False
    return res


def generate_first_population(): #génére la 1er génération de scorpion avec des valeurs aléatoireq
    listAllPop=[]
    for i in range (0,NUMBER_OF_SCORPION):
        scorpion = Scorpion()
        listAllPop.append(scorpion)
    return listAllPop

def evaluation(population): #évalue les scoprions pour établir une hiérarchie 
    for pop in population:
        pop.fitness = 0
        longueurVide = longueurAVide(pop.lb,pop.lc)
        longeurDep = longueurDeplacement(pop.lf,pop.lc)
        K = ressortK(pop.youngmodule,pop.coeffpoisson)
        masseProjec = masseProjectile(pop.p,pop.b,pop.h,pop.lf)

        velo = velocite(K,longeurDep,masseProjec)
        enerImpact = energieImpact(masseProjec,velo)

        pop.d = portee(velo,pesanteur,pop.a)
        if is_rupture(longeurDep,pop.b,pop.h,K,pop.lb,pop.youngmodule)==True:
            
            pop.isRupture = True
            pop.fitness = pop.fitness-5000
        else : 
            pop.fitness = pop.fitness+5000
            pop.isRupture = False
            
        
        if is_tire(longueurVide,pop.lf,pop.lc,pop.lb)==False: #si le tire est possible
            pop.fitness = pop.fitness-5000
            pop.isTire = False
        else : 
            pop.isTire = True
            pop.fitness = pop.fitness + 5000
        
        if pop.d > DISTANCE_SHOOT_FITNESS == False: #si la distance de tire est inférieur a la variable
            pop.fitness = pop.fitness -5000
        else:
            pop.fitness = pop.fitness +5000
        pop.fitness = pop.fitness + enerImpact
    population.sort(key=lambda x: x.fitness,reverse=True)
    return population

def tournament_selection(listAllPop): #permet de choisir les meilleurs ensemble
    pops = listAllPop
    popsSelected=[]
    for i in range(0,int(len(listAllPop)/2)):
        popsSelected.insert(i,[pops[i],pops[i+1]])
    return popsSelected

def exchangeProp(index,scorpionChild1,scorpionChild2): #échange une des 12 propriétés
    if index == 1:
        tmp = scorpionChild1.lb
        scorpionChild1.lb = scorpionChild2.lb
        scorpionChild2 = tmp
    if index == 2:
        tmp = scorpionChild1.b
        scorpionChild1.b = scorpionChild2.b
        scorpionChild2 = tmp
    if index == 3:
        tmp = scorpionChild1.h
        scorpionChild1.h = scorpionChild2.h
        scorpionChild2 = tmp
    if index == 4:
        tmp = scorpionChild1.lc
        scorpionChild1.lc = scorpionChild2.lc
        scorpionChild2 = tmp
    if index == 5:
        tmp = scorpionChild1.lf
        scorpionChild1.lf = scorpionChild2.lf
        scorpionChild2 = tmp
    if index == 6:
        tmp = scorpionChild1.a
        scorpionChild1.a = scorpionChild2.a
        scorpionChild2 = tmp
    if index == 7:
        tmp = scorpionChild1.p
        scorpionChild1.p = scorpionChild2.p
        scorpionChild2 = tmp
    if index == 8:
        tmp = scorpionChild1.bf
        scorpionChild1.bf = scorpionChild2.bf
        scorpionChild2 = tmp
    if index == 9:
        tmp = scorpionChild1.hf
        scorpionChild1.hf = scorpionChild2.hf
        scorpionChild2 = tmp
    if index == 10:
        tmp = scorpionChild1.df
        scorpionChild1.df = scorpionChild2.df 
        scorpionChild2 = tmp
    if index == 11:
        tmp = scorpionChild1.youngmodule
        scorpionChild1.youngmodule = scorpionChild2.youngmodule
        scorpionChild2 = tmp
    if index == 12:
        tmp = scorpionChild1.coeffpoisson
        scorpionChild1.coeffpoisson = scorpionChild2.coeffpoisson
        scorpionChild2 = tmp
    
def mutate(index,scorpion): #change aléatoirement une des 2 propriétées
    if index == 1:
        scorpion = rand.uniform(50, 100)
    if index == 2:
        scorpion= rand.uniform(1, 100)
    if index == 3:
        scorpion = rand.uniform(0.1, 0.5)
    if index == 4:
       scorpion = rand.uniform(1, 49)
    if index == 5:
        scorpion =  rand.uniform(0.1, 0.5)
    if index == 6:
        scorpion = rand.randrange(1, 180)
    if index == 7:
        scorpion = rand.uniform(0.1, 1)
    if index == 8:
        scorpion = rand.uniform(1, 100)
    if index == 9:
        scorpion =rand.uniform(1, 100)
    if index == 10:
        scorpion = rand.uniform(1, 50) 
    if index == 11:
        scorpion = rand.randrange(1, 100) 
    if index == 12:
        scorpion = 0.2
def enjambement(pops): #échnage de propriétés entre les couples
    popFilles=[]
    #Aléatoire entre 6 (50%) et 10 (80%) des paramètres pour voir combien de paramètres sont à échanger.
    for pop in pops:
        numberPropsToChange=rand.randrange(6, 10) # pour ce nb faire ; rand 1 a 12 changer
        indexChange.clear()
        for i in range (0,numberPropsToChange):
            randomProperty=rand.randrange(1, 12)
            if randomProperty in indexChange:
                while randomProperty in indexChange:
                    randomProperty=rand.randrange(1, 12)
            exchangeProp(randomProperty,pop[0],pop[1])
            indexChange.append(randomProperty)
        popFilles.insert(0,pop[0])
        popFilles.insert(0,pop[1])
    indexChange.clear()
    
    return(popFilles)

def mutation(pops): 
    for pop in pops : 
        random_number=rand.randint(0,100)#1% de chance de changer 1 propriétée
        if random_number==1:
            random_number=rand.randint(1,12)
            mutate(random_number,pop)
    return pops

def condition(pops):
    res = False
    pops.sort(key=lambda x: x.fitness,reverse=True)
    if pops[0].d > DISTANCE_SHOOT_CONDITION and pops[0].fitness > FITNESS_SCORE_CONDITION and pops[0].isTire == True and pops[0].isRupture == False: # si le meileur scorpion a ces valeurs
        res = True
    return res

def get_new_pop(listAllPop):
    listAllPop.sort(key=lambda x: x.fitness,reverse=False) #Met en premier dans la liste, les scorpions ayant le moins de Fitness
    for i in range (0,int(len(listAllPop)/2)):
        newScorpion = Scorpion()
        listAllPop[i]=newScorpion #On remplace ce scorpion par un nouveau
    listAllPop.sort(key=lambda x: x.fitness,reverse=True)#Met en premier dans la liste, les scorpions ayant le plus de Fitness
    return listAllPop

graphDistance = matplotlib.pyplot 
listAllPop=generate_first_population()#génération de la 1er génération


while condition(listAllPop) == False: # tant que les conditions ne sont pas réunis
    arrayEval = evaluation(listAllPop) #évalue les scorpions
    arrayTournament = tournament_selection(arrayEval)# défini les couples
    listAllPop = enjambement(arrayTournament) #modification des propriétées entre les couples
    evaluation(listAllPop)# évaluation
    mutation(listAllPop)#mutaion 1% de chance de changer une propriétée au hasard
    listAllpop = get_new_pop(listAllPop)# ajout d'un nouvelle échantillon de scorpion
    listAllPop.sort(key=lambda x: x.fitness,reverse=True) #Met en premier dans la liste, les scorpions ayant le plus de Fitness
    arrayDistance.append(listAllPop[0].d) #ajoute la distance de tir du scorpion a la liste
graphDistance.plot(arrayDistance)
graphDistance.ylabel('Distance en mètre')
graphDistance.show()#montre le graphique de l'évolution de la distance du tir des scorpions en fonction de chaque génération
print("Distance du scorpion avec le meilleur score de fitness : "+str(listAllPop[0].d) + " mètres")
print("Score de fitness : "+str(listAllPop[0].fitness))
print("Hauteur section bras : "+str(listAllPop[0].h))
print("Longueur du bras : "+str(listAllPop[0].lb))
print("Longueur corde : "+str(listAllPop[0].lc))

