# Imports
import time
import ivy.std_api as ivy
import pygame
from math import pi
clock_interval = 30


#==========MANCHE=========================#
Pmax=pi/12 # 15 degrés/sec
nzmax=1

pygame.init()

def from_stick():
    """Récupération des données brutes du joystick \n Renvoie nz,p AP off
    """    
    clock = pygame.time.Clock()
    init = False
    axe_p  = 0
    axe_nz = 1
    axe_nx = 2

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                if not init:
                    init_info(joystick)
                print(f"Joystick {joystick.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joystick[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Position angulaires
        brut_p = joystick.get_axis(axe_p)
        brut_nz = joystick.get_axis(axe_nz)
        brut_nx = joystick.get_axis(axe_nx) # nx ou flap ????
        
        # Boutons
        gachette = joystick.get_button(0)
        bouton_gauche=joystick.get_button(1) # Landing gear ??
        bouton_droit=joystick.get_button(2) # change nx , flap ??
        
        #Debug
        # print(f"bp : {brut_p}\t bnz : {brut_nz}\t bnx : {brut_nx}\t bGachette : {gachette}\t bBGauche : {bouton_gauche}\t bBDroit : {bouton_droit}\n")
            # ivy.IvyBindMsg(from_stick,"Time t=(\S+)")

        #Traitement de l'information
        nz = brut_nz*nzmax
        p = brut_p * Pmax    # ivy.IvyBindMsg(from_stick,"Time t=(\S+)")

        AP_off = gachette
        
        if abs(brut_p) <= 0.1 :
            p = 0
        if abs(brut_nz) <= 0.1 :
            nz = 0
        #Envoi sur ivy

        ivyShare(nz+1,p,AP_off)
    
        clock.tick(clock_interval)


def init_info(joystick):
    print(f"Manette initialisé : {joystick.get_init()}\n")
    print(f"Manette nom : {joystick.get_name()}\n")
    print(f"Manette axes : {joystick.get_numaxes()}\n")
    print(f"Manette bouttons : {joystick.get_numbuttons()}\n")
    print(f"Manette balls : {joystick.get_numballs()}\n")
    print(f"Manette hats : {joystick.get_numhats()}\n")  
    return 
   
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent,_id):
    pass


    

def ivyShare(nz,p,AP_off):
    """Envoi des messages sur le bus ivy"""
    print(f"p : {p}\t nz : {nz}\t AP : {AP_off}\n") #debug
    
    if AP_off:
        ivy.IvySendMsg("MancheAP push")
    ivy.IvySendMsg(f"MancheCmdAxes nz={nz} p={p}") 
    #ivy.IvyStop()

def launch():
    app_name = "Manche"
    ivy_bus = "127.255.255.255:2010" # adresse de broadcast sur le port 2010

    ivy.IvyInit( app_name , "[%s ready ]" % app_name , 0, on_cx_proc ,on_die_proc ) 
    ivy.IvyStart ( ivy_bus )
    time.sleep(1.0)
    # ivy.IvyBindMsg(from_stick,"Time t=(\S+)")
    from_stick()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.    
    pygame.quit()

launch()