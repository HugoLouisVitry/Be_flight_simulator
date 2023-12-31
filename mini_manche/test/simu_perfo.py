import time
from ivy.std_api import *

def on_cx_proc (agent , connected ) :
    pass
def on_die_proc (agent , _id ):
    pass
def on_time(agent, *larg):
    if float(larg[0]) < 10:
        nx_neg=-0.1
        nz_neg=-0.1
        nx_pos=0.01
        nz_pos=0.01
    elif 20<float(larg[0])<30:
        nx_neg=-0.01
        nz_pos=0.01
        nx_neg=-0.1
        nz_pos=0.1
    else:
        nx_neg=-1
        nz_neg=-1
        nx_pos=1
        nz_pos=1
    IvySendMsg (f"nx_neg={nx_neg} nz_neg={nz_neg} nx_pos={nx_pos} nz_pos={nz_pos}")
    
def on_message(agent, *larg):
    IvySendMsg ("APNxControl nx=1")
    IvySendMsg ("APNzControl nz=1")
    IvySendMsg("MagneticDeclination=(13,31)")
    IvySendMsg("WindComponent VWind=10 dirWind=35")
    IvySendMsg("LimitsN nx_neg=2 nx_pos=2 nz_neg=2 nz_pos=2")
    IvySendMsg("LimitsNAP nx_neg_AP=2 nx_pos_AP=2 nz_neg_AP=2 nz_pos_AP=2")
    IvySendMsg("SpeedLimits vmin=100 vmax=250")
    IvySendMsg("ManagedSpeed vi=130")
    IvySendMsg("RollLimits phimax=45 pmax=20")
    IvySendMsg("RollLimitsAP phimax_AP=60 pmax_AP=20")
    IvySendMsg("ManagedAlt alt=60000 Q=1013")

### Ivy Bus
app_name = "Minimancheperfo "
ivy_bus = "127.255.255.255:2010 "
IvyInit ( app_name , # application name for Ivy
"[%s ready ]" % app_name , # ready message
0, # main loop is local
on_cx_proc , # called on cx/ disconnect
on_die_proc ) # called when the agent dies
IvyStart ( ivy_bus )
IvyBindMsg(on_time, '^Time t=(.*)')
IvyBindMsg(on_message, "^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")

# attente pour qu ’ivy s’ initialise correctement
time . sleep (1.0)
