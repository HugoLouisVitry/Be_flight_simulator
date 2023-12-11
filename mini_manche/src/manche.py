# Imports
import time
import ivy.std_api as ivy
import pygame
from math import pi, radians
clock_interval = 30


#==========MANCHE=========================#
Pmax= radians(5) # 5 degrés/sec
nzmax=1

# Variables globales 
Manual=False
p=0
nz=1
pygame.init()

def from_stick(agent, *larg):
    """Récupération des données brutes du joystick \n Modifie nz,p AP off
    """    
    clock = pygame.time.Clock()
    init = False
    axe_p  = 0
    axe_nz = 1
    axe_nx = 2
    
    joystick = pygame.joystick.Joystick(0)

    # Positions angulaires
    brut_p = joystick.get_axis(axe_p)
    brut_nz = joystick.get_axis(axe_nz)
    brut_nx = joystick.get_axis(axe_nx) # nx ou flap ????

    # Boutons
    gachette = joystick.get_button(0)
    bouton_gauche=joystick.get_button(1) # Landing gear ??
    bouton_droit=joystick.get_button(2) # change nx , flap ??

    #Debug
    # print(f"bp : {brut_p}\t bnz : {brut_nz}\t bnx : {brut_nx}\t bGachette : {gachette}\t bBGauche : {bouton_gauche}\t bBDroit : {bouton_droit}\n")

    #Traitement de l'information
    global nz
    global p
    global Manual

    nz = brut_nz*nzmax
    p = brut_p * Pmax

    #Dead zone
    if abs(brut_p) <= 0.1 :
        p = 0
    if abs(brut_nz) <= 0.1 :
        nz = 0

    #Désactivation autopilote
    if  not Manual and gachette==1:
        Manual = True
        ivy.IvySendMsg("MancheAP push")

    #Envoi des commandes manuelles
    if Manual :
        ivy.IvySendMsg(f"MancheCmdAxes nz={nz+1} p={p}")

def on_AP_pushed(agent, *larg):
    global Manual
    Manual = False


#
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent,_id):
    pass

app_name = "Manche"
default_ivy_bus = "127.255.255.255:2010"

def launch_manche(ivy_bus=default_ivy_bus):
    """
    Default bus is 127.255.255.255:2010\n
    Enter the bus as a string "adrress"
    """
    print(f"Ivy started on bus {ivy_bus}\n")
    ivy.IvyInit( app_name , "[%s ready ]" % app_name , 0, on_cx_proc ,on_die_proc ) 
    ivy.IvyStart ( ivy_bus )
    time.sleep(1.0)
    ivy.IvyBindMsg(from_stick,"^Time t=(\S+)")
    ivy.IvyBindMsg(on_AP_pushed,"^FCUAP1 on")
    print("Ready")

if __name__ == "__main__":
    launch_manche()

    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.    
