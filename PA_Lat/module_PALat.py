from ivy.std_api import *
import time
import numpy as np

deg2rad = np.pi / 180
# Variables globales

state_vector = None
wind_vector = [50, 0]
magnetic_Declinaison_vector = [0 * 13.69]
limit_factor_vector = None
roll_limits_AP_vector = [30 * deg2rad, 10000]
axis_vector = [0, 0, 90]
fcu_lat_vector = ['Managed', 90]


# Fonctions

def null_cb(*a):
    pass


def state(agent, *larg):
    global state_vector
    state_vector = np.float_(larg)


def wind(agent, *larg):
    global wind_vector
    wind_vector = np.float_(larg)



def magnetic_declinaison(agent, *larg):
    global magnetic_Declinaison_vector
    magnetic_Declinaison_vector = np.float_(larg)


def limit_factor(agent, *larg):
    global limit_factor_vector
    limit_factor_vector = np.float_(larg)


def roll_limits_AP(agent, *larg):
    global roll_limits_AP_vector
    roll_limits_AP_vector = deg2rad * np.float_(larg)

def axis(agent, *larg):
    global axis_vector
    axis_vector = np.float_(larg)
    print(magnetic_Declinaison_vector[0])
    if fcu_lat_vector[0] == 'SelectedHeading':
        capture_cap((float(fcu_lat_vector[1]) ) * deg2rad+ magnetic_Declinaison_vector[0])
    elif fcu_lat_vector[0] == 'SelectedTrack':
        capture_route((float(fcu_lat_vector[1])) * deg2rad + magnetic_Declinaison_vector[0])
    elif fcu_lat_vector[0] == 'Managed':
        capture_axe()


def fcu_lat(agent, *larg):
    global fcu_lat_vector
    fcu_lat_vector = larg


IvyInit("IvyGetMsgApp", "Ready", 0, null_cb, null_cb)
IvyStart("127.255.255:2010")

## Commande pour récuperer les données
# State Vector
IvyBindMsg(state, '^StateVector x=(.*) y=(.*) z=(.*) Vp=(.*) fpa=(.*) psi=(.*) phi=(.*)')
# Vent
IvyBindMsg(wind, '^WindComponent VWind=(.*) dirWind=(.*)')
# Déclinaison magnetique
IvyBindMsg(magnetic_declinaison, '^MagneticDeclination=(.*)')
# Limites facteur de charge
IvyBindMsg(limit_factor, '^LimitsN nx=(.*) nz=(.*) nx_AP=(.*) nz_AP=(.*)')
# Angle et vitesse de roulis AP
IvyBindMsg(roll_limits_AP, '^RollLimitsAP phimax_AP=(.*) pmax_AP=(.*)')
# Axe à capturer
IvyBindMsg(axis, '^Axis x=(.*) y=(.*) chi=(.*)')
# FCU : modes latéraux
IvyBindMsg(fcu_lat, '^FCULateral Mode=(.*) Val=(.*)')

############################################################################
## DIFFERENTES CAPTURES
# Vecteur d'état: state_vector[x,y,z,tas,fpa,psi,phi]; tas(m/s), fpa(degré), psi(degré), phi(degré), x,y,z en mètre
g = 9.81
tauphi = 1
taupsi = 10
tauEy = 100


## capture de phi
def capture_phi(phic):
    # limite sur phi
    if phic > roll_limits_AP_vector[0]:  # and phic>=0:
        phic = roll_limits_AP_vector[0]
    elif phic < -roll_limits_AP_vector[0]:  # and phic<0:
        phic = -roll_limits_AP_vector[0]
    phidot = (phic - state_vector[6]) / tauphi

    # limite sur phi dot
    if phidot > roll_limits_AP_vector[1]:  # and phidot>=0:
        phidot = roll_limits_AP_vector[1]
    elif phidot < -roll_limits_AP_vector[1]:  # and phidot<0:
        phidot = -roll_limits_AP_vector[1]

    IvySendMsg("APLatpControl p=%s" % phidot)


## capture de cap
def capture_cap(psiC):
    deltaCap = psiC - state_vector[5]
    while deltaCap >= np.pi:
        deltaCap -= 2 * np.pi
    while deltaCap < -np.pi:
        deltaCap += 2 * np.pi
    phic = (deltaCap) * state_vector[3] / (g * taupsi)

    capture_phi(phic)


## route
def capture_route(Xc):
    psiR = Xc - derive()
    capture_cap(psiR)


## axe
def capture_axe():
    Xcapture = Xcapture_fct()
    capture_route(Xcapture)


############################################################################
## FONCTIONS UTILISES

## ground speed
def ground_speed():
    x_dot = state_vector[3] * np.cos(state_vector[4]) * np.cos(state_vector[5]) - wind_vector[0] * np.cos(
        wind_vector[1] )
    y_dot = state_vector[3] * np.cos(state_vector[4]) * np.sin(state_vector[5]) - wind_vector[0] * np.sin(
        wind_vector[1] )
    return ((x_dot) ** 2 + (y_dot) ** 2) ** 0.5


## derive
def derive():
    X = np.arctan2(
        state_vector[3] * np.cos(state_vector[4]) * np.sin(state_vector[5]) + wind_vector[0] * np.sin(wind_vector[1]  + np.pi),
        state_vector[3] * np.cos(state_vector[4])  * np.cos(state_vector[5]) + wind_vector[0] * np.cos(wind_vector[1]  + np.pi))
    a = X - wind_vector[1]
    sind = wind_vector[0] * np.sin(a) / state_vector[3] * np.cos(state_vector[4])
    if sind > 1:
        sind = 1
    elif sind < -1:
        sind = -1
    print(np.arcsin(sind))
    return np.arcsin(sind)


## fonction e qui permet à l'avion de capturer l'axe en distance
def ey_fct():
    ey = -np.sin(axis_vector[2] * deg2rad) * (state_vector[0] - axis_vector[0]) + np.cos(axis_vector[2] * deg2rad) * (
                state_vector[1] - axis_vector[1])
    print('ey = ' + str(ey))
    return ey


## fonction qui permet à l'avion de capturer l'axe en cap
def Xcapture_fct():
    gs = ground_speed()
    sinX = -ey_fct() / (tauEy * gs)
    if sinX > 1:
        sinX = 1
    elif sinX < -1:
        sinX = -1
    X = np.arcsin(sinX)
    Xcapture = X + axis_vector[2] * deg2rad
    print('Xcapture = ' + str(Xcapture / deg2rad))
    return Xcapture


IvyMainLoop()

IvyStop()
