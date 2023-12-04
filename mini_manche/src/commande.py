import ivy.std_api as ivy
import time

# Configuration Ivy
AppName = "Commande"
Ivy_bus = "127.255.255.255:2010" #TODO à changer pour travailler entre plusieurs ordinateurs

def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent, _id):
    pass

# Variable globale
autoPiloteStatus = "off"

# Fonction message
def on_MancheAP(agent, *larg): # Désactive l'autopilote en cas d'appuie du bouton au manche
    autoPiloteStatus = "off"
    ivy.IvySendMsg("FCUAP1 off")

def on_FCUAP1_push(agent, *larg): # Change l'état de l'autopilote (on/off) en cas d'appuie du bouton FCU
    global autoPiloteStatus
    if autoPiloteStatus == "on":
        autoPiloteStatus = "off"
    else:
        autoPiloteStatus = "on"
    ivy.IvySendMsg(f"FCUAP1 {autoPiloteStatus}")

def on_MancheCommand(agent, *larg): # [nz,p] Update la commande du manche
    return 



if __name__ == "__main__":
    ivy.IvyInit(AppName, f"[{AppName} ready]", 0, on_cx_proc, on_die_proc)
    ivy.IvyStart(Ivy_bus)
    time.sleep(1)

    # Gestion de autoPiloteStatus
    ivy.IvyBindMsg(on_MancheAP, "^MancheAP push")
    ivy.IvyBindMsg(on_FCUAP1_push, "^FCUAP1 push")

    # Gestion des données du manche
    ivy.IvyBindMsg(on_MancheCommand,"^") #TODO Mettre le format du message (nz+p)



