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
