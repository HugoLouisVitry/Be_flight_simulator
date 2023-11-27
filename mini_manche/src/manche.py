# Imports

import ivy.std_api as ivy
import pygame

clock_interval = 30
Pmax=50
nzmax=2

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
                print(f"Joystick {joystick.get_instance_id()} connencted")

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
       # print(f"p : {brut_p}\t nz : {brut_nz}\t nx : {brut_nx}\t Gachette : {gachette}\t BGauche : {bouton_gauche}\t BDroit : {bouton_droit}\n")
        
        #Traitement de l'information
        nz = brut_nz*nzmax
        p = brut_p * Pmax
        AP_off = gachette
        
        #Envoi sur ivy
        ivyShare(nz,p,AP_off)
        clock.tick(clock_interval)

def ivyShare(nz,p,AP_off):
    """Envoi des messages sur le bus ivy"""
    print(f"p : {p}\t nz : {nz}\t AP : {AP_off}\n")
    #envoyer "MancheAP push" a quentin ( no args )
    #envoyer "MancheCmdAxes nz= p="
    pass
    

def init_info(joystick):
    print(f"Manette initialisé : {joystick.get_init()}\n")
    print(f"Manette nom : {joystick.get_name()}\n")
    print(f"Manette axes : {joystick.get_numaxes()}\n")
    print(f"Manette bouttons : {joystick.get_numbuttons()}\n")
    print(f"Manette balls : {joystick.get_numballs()}\n")
    print(f"Manette hats : {joystick.get_numhats()}\n")  
    return 
   



if __name__ == '__main__':
    from_stick()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.    
    pygame.quit()
