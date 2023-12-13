import ivy.std_api as ivy
import time
import math

# InitStateVector x=0 y=0 z=2000 Vp=180 fpa=0 psi=0 phi=0

# Configuration Ivy
AppName = "Commande"
Ivy_bus = "127.255.255.255:2010" #TODO à changer pour travailler entre plusieurs ordinateurs

def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent, _id):
    pass

# Constante
Dt = 2 # Constante de temps pour lisser la limitation dû à phi_limite_FGS
back_angle = math.radians(33)
marge_angle = math.radians(5)
tau_back = 1 # Tau pour le retour à 33° de roulis en manuel

# Variable globale reçue
nz_manche = 1. # Commande brute
p_manche = 0. # Commande brute
nz_max = 2. # Limite brute
nz_min = 0. # Limite brute
phi_limite_FGS = math.pi/4 # en radians
p_limite_FGS = math.pi/16 # en radians/s
phi = 0. # en radians

# Variable globale interne
autoPiloteStatus = "off"
back_to_rest = False # Booléen pour le retour à +/- 33° de roulis au lâcher du mini manche

# Fonction message
def on_MancheAP(agent, *larg): # Désactive l'autopilote en cas d'appuie du bouton au manche
    global autoPiloteStatus 
    autoPiloteStatus = "off"
    ivy.IvySendMsg("FCUAP1 off")

def on_FCUAP1_push(agent, *larg): # Change l'état de l'autopilote (on/off) en cas d'appuie du bouton FCU
    global autoPiloteStatus
    if autoPiloteStatus == "on":
        autoPiloteStatus = "off"
    else:
        autoPiloteStatus = "on"
    ivy.IvySendMsg(f"FCUAP1 {autoPiloteStatus}")

def on_MancheCmdAxes(agent, *larg): # [nz,p] Update la commande brute du manche
    global nz_manche, p_manche
    nz_manche = float(larg[0])
    p_manche = float(larg[1])

def on_LimitsN(agent,*larg): # Ignore la limitation en nx car non commandé par le manche
    global nz_min, nz_max
    nz_max = float(larg[2])
    nz_min = float(larg[3])

def on_RollLimits(agent,*larg):
    global phi_limite_FGS, p_limite_FGS
    phi_limite_FGS = math.radians(float(larg[0])) # Convertion deg -> rad nécessaire
    p_limite_FGS = math.radians(float(larg[1]))

def on_StateVector(agent,*larg): # Stocke la valeur de phi
    global phi  
    phi = float(larg[6])
    
def on_APLongNxControl(agent, *larg): # Transmet directement la commande nx au modèle avion
    nx = float(larg[0])
    ivy.IvySendMsg(f"APNxControl nx={nx}")

def on_APLongNzControl(agent, *larg):
    nz_AP = float(larg[0])
    if autoPiloteStatus == "on":
        nz = nz_AP
    else:
        nz = max(nz_min,min(nz_max,nz_manche)) # Limitation de la commande nz manche
    ivy.IvySendMsg(f"APNzControl nz={nz}")

def on_APLatpControl(agent,*larg):
    global back_to_rest
    p_AP = float(larg[0])
    if autoPiloteStatus == "on":
        p = p_AP
    else: # Commande manuel
        # Calcul de la limitation de p manuel avec limitation en phi
        p_limit_neg = max(-p_limite_FGS, (-phi_limite_FGS - phi)/Dt)
        p_limit_pos = min(p_limite_FGS, (phi_limite_FGS - phi)/Dt)
        p = max(p_limit_neg,min(p_limit_pos,p_manche))

        # Retour à phi_limite si dépassement
        if phi < -phi_limite_FGS:
            p = - phi_limite_FGS - phi
        elif phi > phi_limite_FGS:
            p = phi_limite_FGS - phi

        # Retour à p = +/- 33° si on relâche le manche après être arrivé en butée
        if p_manche == 0 and back_to_rest :
            if phi < 0: # On suppose que l'on ne dépasse pas 0 lorsque l'on commande phi = +/- 33°
                p = min((-phi - back_angle)/tau_back,p_limit_pos)
            else:
                p = max((back_angle - phi)/tau_back,p_limit_neg)
        
        if abs(abs(phi) - phi_limite_FGS) <= marge_angle : # On arrive en butée de phi -> armement du retour à +/- 33°
            back_to_rest = True
        elif p_manche != 0 : # On n'est plus/pas en butée et il y a une commande manuel -> désarmement du retour à +/- 33°
            back_to_rest = False

    ivy.IvySendMsg(f"APLatControl rollRate={p}")
            


def commande(ivy_bus=Ivy_bus):
    """
    Default bus is 127.255.255.255:2010\n
    Enter the bus as a string : commande("adrress")
    """
    ivy.IvyInit(AppName, f"[{AppName} ready]", 0, on_cx_proc, on_die_proc)
    ivy.IvyStart(Ivy_bus)
    time.sleep(1)

    # Gestion de autoPiloteStatus
    ivy.IvyBindMsg(on_MancheAP, "^MancheAP push")
    ivy.IvyBindMsg(on_FCUAP1_push, "^FCUAP1 push")

    # Gestion des données du manche
    ivy.IvyBindMsg(on_MancheCmdAxes,"^MancheCmdAxes nz=(\S+) p=(\S+)")

    # Gestion des limites brute FGS
    ivy.IvyBindMsg(on_LimitsN,"^LimitsN nx_neg=(\S+) nx_pos=(\S+) nz_neg=(\S+) nz_pos=(\S+)")
    ivy.IvyBindMsg(on_RollLimits,"^RollLimits phimax=(\S+) pmax=(\S+)")

    # Reception et envoie des commandes au modèle avion
    # APLongitudinale
    ivy.IvyBindMsg(on_APLongNxControl,"^APLongNxControl nx=(\S+)")
    ivy.IvyBindMsg(on_APLongNzControl,"^APLongNzControl nz=(\S+)")
    # APLateral
    ivy.IvyBindMsg(on_APLatpControl,"^APLatpControl p=(\S+)")
    
    ivy.IvyBindMsg(on_StateVector,"^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
    

if __name__ == "__main__":
    commande()


