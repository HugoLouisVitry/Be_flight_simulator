from os import cpu_count
from pickle import TRUE
from traceback import print_tb
from xml.dom.minidom import TypeInfo
from ivy.std_api import *
import time
import numpy as np 
import matplotlib.pyplot as plt
state_vector_init=False
limits_init = False
v_lim_init = False
cap_v= False
cap_pente =False
alt_mode = "Managed" #Selected ou FPA ou VS
v_mode = "Managed" #Selected ou Managed
alt_c=0
v_c_TAS=0
fpa_vz_c=0
k11 = 0.08
k22 = 2
nx_min =0
nx_max =0
nz_min =0
nz_max =0
nz=1
nx=0
v_lim=[0,0]
state_vector = {"x":0,"y":0,"z":0,"Vp":0,"fpa":0,"phi":0,"psi":0}

def op(agent, connected):
    pass
def deg2rad(x):
    return x*np.pi/180

def cl(agent,_id):
    IvyStop()


def apply_lim(value, min, max):
    if value>max:
        return max
    elif value < min:
        return min
    else: 
        return value
    
def calculer_vitesse_TAS(IAS,z):
    TAS = IAS + 0.01 * IAS * z/600 #Pour passer directement de l'IAS à la TAS: plus 1% de IAS par tranche de 600ft d'altitude 
    return TAS

def set_limits(agent,*larg):
    global nx_min,nx_max,nz_min,nz_max, limits_init
    nx_min = float(larg[0])
    nx_max = float(larg[1])
    nz_min = float(larg[2])   
    nz_max = float(larg[3])
    limits_init = True

def maj_vitesse(agent, *larg):
    global v_lim, v_lim_init
    v_lim[0],v_lim[1]=float(larg[0]),float(larg[1])
    v_lim_init=True

def maj_state_v(agent, *larg):
    global state_vector, alt_c, v_c_TAS ,state_vector_init
    state_vector = {"x":float(larg[0]),"y":float(larg[1]),"z":float(larg[2]),"Vp":float(larg[3]),"fpa":(float(larg[4])),"psi":(float(larg[5])),"phi":(float(larg[6]))}
    alt_c =state_vector["z"]
    v_c_TAS = state_vector["Vp"]
    state_vector_init=True
    if cap_v :
        if v_mode=="Managed":
            capture_vitesse_managed()
        elif v_mode=="Selected":
            capture_vitesse()
    if cap_pente:
        if alt_mode == "FPA" or alt_mode=="Selected" or alt_mode =="VS":
            capture_pente()
        elif alt_mode =="Managed":
            capture_pente_managed()
    else:
        send() 


    
def capture_pente(agent=0, *larg):
    epsilon = 1 #tolérance en m/s  
    global alt_c,fpa_vz_c,alt_mode , nz,v_c_TAS, cap_pente
    if larg:
        alt_c = float(larg[0])
        alt_mode = larg[1]
        fpa_vz_c = float(larg[2])
    else:
        pass
    if (abs(v_c_TAS-state_vector["Vp"])>epsilon or not state_vector_init or not limits_init or not v_lim_init ):
        cap_pente = True
        send()
        return
        
    
    elif alt_mode == "Selected":
        nz = ((alt_c-state_vector["z"])/state_vector["Vp"]*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
        nz = apply_lim(nz,nz_min,nz_max)
        send()
        cap_pente=False
    elif alt_mode == 'FPA':
        nz = (((fpa_vz_c - state_vector["fpa"])*k22) + np.cos(state_vector["fpa"]))/np.cos(state_vector["phi"])
        nz = apply_lim(nz,nz_min,nz_max)
        send() 
        cap_pente= False
    elif alt_mode == 'VS':
        nz = (((np.arcsin(fpa_vz_c/state_vector["Vp"]) - state_vector["fpa"])*k22) + np.cos(state_vector["fpa"]))/np.cos(state_vector["phi"])
        nz = apply_lim(nz,nz_min,nz_max)
        send()
        cap_pente= False
    else:
         print("Error capt pente")

         
def capture_pente_managed(agent=0, *larg):
    global alt_c, nz,cap_pente
    if larg:
        alt_c = float(larg[0])
        alt_mode="Managed"
    else:
        pass
    epsilon = 1 #tolérance en m/s  
    if (abs(v_c_TAS-state_vector["Vp"])>epsilon or not state_vector_init or not limits_init or not v_lim_init ):
        cap_pente=True
        send()
        return
    elif alt_mode == "Managed":

        nz = ((alt_c-state_vector["z"])/state_vector["Vp"]*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
        nz = apply_lim(nz,nz_min,nz_max)
        send()
        cap_pente = False
    else:
        print("Error capt pente managed")

def capture_vitesse(agent=0, *larg):
    global alt_c, nx, v_mode, v_c_TAS, cap_v
    epsilon = 2 #tolérance en m  
    if larg:
        v_c_TAS = calculer_vitesse_TAS(float(larg[1]),state_vector["z"])
        v_mode = larg[0]
    else:
        pass
    if (abs(alt_c-state_vector["z"])>epsilon  or not state_vector_init or not limits_init or not v_lim_init ):
        cap_v=True
        send()
        return
    
    if v_mode == "Selected":
        nx = (apply_lim(v_c_TAS,v_lim[0],v_lim[1]) - state_vector["Vp"])*k11 + np.sin(state_vector["fpa"])
        nx = apply_lim(nx,nx_min,nx_max)
        send()
        cap_v= False
    else: 
        print("Error capt vitesse") #on attend de recevoir le message du fgs avec la vitesse managed

def capture_vitesse_managed(agent=0, *larg):
    global v_c_TAS, alt_c, nx,cap_v
    if larg:
        v_c_TAS = float(larg[0])
    else:
        pass
    epsilon = 2 #tolérance en m  
    if (abs(alt_c-state_vector["z"])>epsilon or not state_vector_init or not limits_init or not v_lim_init ):
        cap_v =True
        send()
        return
    nx = (v_c_TAS - state_vector["Vp"])*k11 + np.sin(state_vector["fpa"])
    nx = apply_lim(nx,nx_min,nx_max)
    send()#pas nécessaire apply_lim car déjà verifier par le fgs
    cap_v=False

def send():
    global nz,nx
    print("nz={}".format(nz),"nx={}".format(nx))
    time.sleep(1)
    IvySendMsg("APLongNzControl nz={}".format(nz))
    IvySendMsg("APLongNxControl nx={}".format(nx))

app_n ="PAlong"
ivy_bus ="127.255.255.255:8000"
IvyInit(app_n ,"Pa_long_ready" ,0 ,op ,cl )
IvyStart(ivy_bus)
time.sleep(1)
IvyBindMsg(maj_state_v,"^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
IvyBindMsg(set_limits,'^LimitsNAP nx_neg_AP=(\S+) nx_pos_AP=(\S+) nz_neg_AP=(\S+) nz_pos_AP=(\S+)')
IvyBindMsg(maj_vitesse, "^SpeedLimits vmin=(\S+) vmax=(\S+)")
IvyBindMsg(capture_pente_managed,'^ManagedAlt alt=(\S+) Q=(\S+)')
IvyBindMsg(capture_pente,'^FCUVertical Altitude=(\S+) Mode=(\S+) Val=(\S+)') ## val prend une Vz ou une FPA
IvyBindMsg(capture_vitesse,'^FCUSpeedMach Mode=(\S+) Val=(\S+)')
IvyBindMsg(capture_vitesse_managed,"^ManagedSpeed vi=(\S+)")
IvyMainLoop()
