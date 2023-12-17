# Imports
import time
import ivy.std_api as ivy
import pygame
from math import pi, radians
import threading as tr
import sys
clock_interval = 30


#==========MANCHE=============#
Pmax= radians(5) # 5 degrés/sec
nzmax=1


#### Variables globales ####

#joystick
gachette=0
PUSHED=1
DEAD_axe_0 = 0.13
DEAD_axe_1 = 0.1

# AP, p, nz,nx
Manual=True
p=0
nz=1
dnx=0
change_dnx=False
DNX=0.05# on envoie un delta nx
auto_nx = "False"
change_nx_mode = False
#Flaps
flap = 0
change_flap=False

#Landing Gear
LDG_IN = 0
LDG_OUT = 1
ldg = LDG_IN
change_ldg = False

#Mode pour les boutons 
IDLE = "IDLE"
NX = "NX"
FLAP = "FLAP"
LDG = "LDG"
AUTO_NX = "AUTO_NX"
Button_Mode = IDLE

pygame.init()

def update_stick():
    """
    Joystick handling and interpretation for command entries\n
    Hotplug is handled so you can unplug and plug again the joystick and it will work\n

    You can plug any joystick but it isn't guaranteed to work\n
    Only the ST90 will exactly do what's expected to
    
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
        axe_mode = 2

        global nz
        global p
        global Manual
        global gachette
        global Button_Mode
        
        for joystick in joysticks.values():

            # Positions angulaires et voyants
            brut_p = joystick.get_axis(axe_p)
            brut_nz = joystick.get_axis(axe_nz)
            mode_axe = joystick.get_axis(axe_mode)

            # Boutons
            gachette = joystick.get_button(0)
            bouton_gauche=joystick.get_button(1)
            bouton_droit=joystick.get_button(2)

            #Debug
            #print(f"bp : {brut_p}\t bnz : {brut_nz}\t bnx : {brut_nx}\t bGachette : {gachette}\n")# bBGauche : {bouton_gauche}\t bBDroit : {bouton_droit}\n")

            #Traitement de l'information
            nz = brut_nz*nzmax
            p = brut_p * Pmax

            #Dead zone
            if abs(brut_p) <= DEAD_axe_0 :
                p = 0
            if abs(brut_nz) <= DEAD_axe_1:
                nz = 0
                
            # Valeur de l'axe bouton (1,0.498 or 0.506,-0.004,-0.498 or -0.506,-1)
            match round(mode_axe,1):
                case 0:
                    Button_Mode = FLAP
                case -0.5:
                    Button_Mode = LDG
                case 0.5:
                    Button_Mode = NX
                case -1:
                    Button_Mode = AUTO_NX
                case _:
                    Button_Mode = IDLE

            #Controle flaps, ldg et nx
            mode_control(Button_Mode,bouton_gauche,bouton_droit)
                    
            
                
def mode_control(mode,minus,add):
    """
    Joystick button configuration handling\n
    Modes are flaps, landing gears and nx.
    """
    global change_dnx
    global dnx
    global flap
    global change_flap
    global ldg
    global change_ldg
    global auto_nx
    global change_nx_mode

    if mode == FLAP :
        #print("FLAP mode")
        if not change_flap:
            if minus == PUSHED and not add:
                if flap > 0 :
                    flap = flap - 1
                    change_flap = True
                #print(f"flap = {flap}\n")
    
            if not minus and add == PUSHED:
                if flap<2:
                    flap = flap + 1
                    change_flap = True
                #print(f"flap = {flap}\n")
               
    elif mode == LDG :
        #print("LDG mode")
        if minus == PUSHED and not add:
            ldg = LDG_IN
            change_ldg=True
            #print("\t ldg_in")
        if not minus and add == PUSHED:
            ldg = LDG_OUT
            change_ldg=True
            #print("\t ldg_out")

    elif mode == AUTO_NX : 
            if minus == PUSHED and not add:
                auto_nx = "False"
                change_nx_mode = True
            if not minus and add == PUSHED:
                auto_nx = "True" 
                change_nx_mode = True       

    elif mode == NX :
        if auto_nx == "False" : 
            #print("NX mode")
            if minus == PUSHED and not add:
                dnx = -DNX
                change_dnx = True
            if not minus and add == PUSHED:
                dnx = DNX
                change_dnx = True
            
    else : #IDLE
        #print("IDLE mode")
        pass
    print(
        f"Mode explanation\n"
        +f"\tIDLE : do nothing\n"
        +f"\tNX : decrease/increase nx value \n"
        +f"\tFLAP : decrease/increase flap config\n"
        +f"\tLDG : put in/out the ldgs\n"
        +f"\tAUTO_NX : disable/enable auto thrust\n\n"
        +f"Actual mode : {mode} \n")

def ivy_share(agent, *larg):
    """
    Send messages on ivy bus in sync with the clock
    
    """
    
    global nz
    global p    
    global Manual
    global gachette
    global change_dnx
    global dnx
    global flap
    global change_flap
    global ldg
    global change_ldg
    global auto_nx
    global change_nx_mode
    
    #Désactivation autopilote
    if  not Manual and gachette==1:
        Manual = True
        #print(f"Manual : {Manual}")
        ivy.IvySendMsg("MancheAP push")

    #Commandes manuelles ed nz et p
    if Manual :
        ivy.IvySendMsg(f"MancheCmdAxes nz={nz+1} p={p}")
        
    #Commande pour le fgs
    if change_dnx :
        ivy.IvySendMsg(f"MancheCmdPoussee dnx={dnx}")
        change_dnx = False
    if change_flap :
        ivy.IvySendMsg(f"MancheFlap f={flap}")
        change_flap = False
    if change_ldg :
        ivy.IvySendMsg(f"MancheLdg ldg={ldg}")
        change_ldg = False
    if change_nx_mode:
        ivy.IvySendMsg(f"MancheThr auto_thr={auto_nx}")
        change_nx_mode = False
        

#Gestion etat AP
def on_AP_on(agent, *larg):
    """
    Handle AP enabling status 
    """
    global Manual
    Manual = False
    #print(f"Manual : {Manual}")
    
def on_AP_off(agent, *larg):
    """
    Handle AP disabling status 
    """
    global Manual
    Manual = True
#    print(f"Manual : {Manual}")

#Ivy
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent,_id):
    pass

app_name = "Manche"
ivy_bus = "127.255.255.255:2010"

if len(sys.argv)==2: # bus de com en paramètres
    ivy_bus = sys.argv[1]

def launch_manche():
    """
    Use this function to start joystick handling\n
    Default bus is 127.255.255.255:2010\n
    Enter the bus as a string "x.x.x.x:x" as a python parrameter
    """
    print(f"Ivy started on bus {ivy_bus}\n")
    ivy.IvyInit( app_name , "[%s ready ]" % app_name , 0, on_cx_proc ,on_die_proc ) 
    ivy.IvyStart ( ivy_bus )
    time.sleep(1.0)
    stick=tr.Thread(target=update_stick)
    stick.start()
    ivy.IvyBindMsg(on_AP_on,"^FCUAP1 on")
    ivy.IvyBindMsg(on_AP_off,"^FCUAP1 off")
    ivy.IvyBindMsg(ivy_share,"^Time t=(\S+)")
    print("Ready")

if __name__ == "__main__":
    launch_manche()

