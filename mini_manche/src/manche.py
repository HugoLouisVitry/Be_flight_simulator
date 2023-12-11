# Imports
import time
import ivy.std_api as ivy
import pygame
from math import pi, radians
import threading as tr
import sys
clock_interval = 30


#==========MANCHE=========================#
Pmax= radians(5) # 5 degrés/sec
nzmax=1


# Variables globales 

Manual=False
p=0
nz=1
gachette=0

pygame.init()

def update_stick():
    """Récupération des données brutes du joystick \n Modifie nz,p AP off
    """
    
    joysticks = {}
    done=False
    while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # Flag that we are done so we exit this loop.

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        joystick = joysticks[event.instance_id]
                        if joystick.rumble(0, 0.7, 500):
                            print(f"Rumble effect played on joystick {event.instance_id}")

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    # This event will be generated when the program starts for every
                    # joystick, filling up the list without needing to create them manually.
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connected")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")
        axe_p  = 0
        axe_nz = 1
        axe_nx = 2

        global nz
        global p
        global Manual
        global gachette

        for joystick in joysticks.values():

            # Positions angulaires
            brut_p = joystick.get_axis(axe_p)
            brut_nz = joystick.get_axis(axe_nz)
            brut_nx = joystick.get_axis(axe_nx) # nx ou flap ????

            # Boutons
            gachette = joystick.get_button(0)
            bouton_gauche=joystick.get_button(1) # Landing gear ??
            bouton_droit=joystick.get_button(2) # change nx , flap ??

            #Debug
            #print(f"bp : {brut_p}\t bnz : {brut_nz}\t bnx : {brut_nx}\t bGachette : {gachette}\n")# bBGauche : {bouton_gauche}\t bBDroit : {bouton_droit}\n")

            #Traitement de l'information
            nz = brut_nz*nzmax
            p = brut_p * Pmax

            #Dead zone
            if abs(brut_p) <= 0.13 :
                p = 0
            if abs(brut_nz) <= 0.1 :
                nz = 0


def ivy_share(agent, *larg):
    
    global nz
    global p
    global Manual
    global gachette
    
    #Désactivation autopilote
    if  not Manual and gachette==1:
        Manual = True
        print(f"Manual : {Manual}")
        ivy.IvySendMsg("MancheAP push")

    #Envoi des commandes manuelles
    if Manual :
        ivy.IvySendMsg(f"MancheCmdAxes nz={nz+1} p={p}")


def on_AP_pushed(agent, *larg):
    global Manual
    Manual = False
    print(f"Manual : {Manual}")

#
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent,_id):
    pass

app_name = "Manche"
ivy_bus = "127.255.255.255:2010"

if len(sys.argv)==2:
    ivy_bus = sys.argv[1]

def launch_manche():
    """
    Default bus is 127.255.255.255:2010\n
    Enter the bus as a string "adrress"
    """
    print(f"Ivy started on bus {ivy_bus}\n")
    ivy.IvyInit( app_name , "[%s ready ]" % app_name , 0, on_cx_proc ,on_die_proc ) 
    ivy.IvyStart ( ivy_bus )
    time.sleep(1.0)
    stick=tr.Thread(target=update_stick)
    stick.start()
    ivy.IvyBindMsg(on_AP_pushed,"^FCUAP1 on")
    ivy.IvyBindMsg(ivy_share,"^Time t=(\S+)")
    print("Ready")

if __name__ == "__main__":
    launch_manche()

    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.    
