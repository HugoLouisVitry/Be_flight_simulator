from ivy.std_api import *
import numpy as np
import time as t
c = 0
def null_cb(*a):
    pass

#Emission des commandes et des init vecteurs
Situation_1 = "InitStateVector x=0 y=0 z=5000 Vp=200 fpa=0 psi=0 phi=0"
Situation_2 = "InitStateVector x=0 y=0 z=500 Vp=200 fpa=5 psi=0 phi=0"
Situation_3 = "InitStateVector x=0 y=0 z=5000 Vp=200 fpa=0 psi=0 phi=0"

Commande_1 = "Axis x=0 y=0 chi=0" #Voir si l'avion reste sur l'axe sur lequel il est
Commande_2 = "Axis x=0 y=0 chi=135" #Test d'une capture d'axe
Commande_3 = "Axis x=0 y=0 chi=180" #Verification qu'il ne dépasse pas le roll max
vent2 = np.deg2rad(90)
Vent_1 = "WindComponent VWind=40 dirWind=0"
Vent_2 = "WindComponent VWind=40 dirWind=%s " %vent2
Vent_3 = "WindComponent VWind=100 dirWind=0"



#Fonctions

def envoie_message(Initial , Vent):
    IvySendMsg(Initial)
    IvySendMsg(Vent)


phidot_mod = None
State_vector_vector = None

def phidot_module(agentMsg , *larg):
    global phidot_mod
    phidot_mod = np.float_(larg)
    IvySendMsg('APLatControl rollRate=%s'%phidot_mod[0] )

declinaison = np.deg2rad(0 * 13.69)
def state_vector(agent, *larg) :
    global State_vector_vector
    global c
    State_vector_vector = np.float_(larg)
    if c ==0 :
        envoie_message(Situation_2, Vent_2)
        IvySendMsg("MagneticDeclination =%s"%declinaison)
        IvySendMsg("RollLimitsAP phi_max = 25 pmax_AP=10")
        IvySendMsg("LimitsN nx=1.3 nz=2 nx_AP=1.3 nz_AP=2 ")
        c = 1

    IvySendMsg(Commande_2)
    with open('vecteur.txt', 'w') as fichier:
    # Convertir chaque élément en chaîne de caractères et les écrire dans le fichier
        for element in State_vector_vector:
            fichier.write(str(element))
        fichier.write(str('\n'))






def timer(agent , *larg):
    global time
    time = 100

#Ivy


IvyInit("IvyAppEmetInitial" , "Ready" , 0,null_cb , null_cb)
IvyStart("127.255.255:2010") #Changement possible pour les tests

#Envoie des constantes (pour toutes situations)




IvyBindMsg(phidot_module, '^APLatpControl p=(.*)')

IvyBindMsg(state_vector, '^StateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)')
IvyBindMsg(timer , '^Time t=100')





IvyMainLoop()
