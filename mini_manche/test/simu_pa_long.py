import time
from ivy.std_api import *

### Ivy Bus
def on_cx_proc (agent , connected ) :
    pass
def on_die_proc (agent , _id ):
    pass
def on_time(agent, *larg):
    if float(larg[0]) < 10:
        p=0.1
    elif 20<float(larg[0])<30:
        p=-0.1
    else: p=0

    IvySendMsg("NxConstante=1.15 NzConstante=0.95")
    IvySendMsg (f"Pcst p={p}")

app_name = "Minimanchetestlongi"
ivy_bus = "127.255.255.255:2010"
IvyInit ( app_name , # application name for Ivy
"[%s ready ]" % app_name , # ready message
0, # main loop is local
on_cx_proc , # called on cx/ disconnect
on_die_proc ) # called when the agent dies
IvyStart ( ivy_bus )
IvyBindMsg(on_time, '^Time t=(.*)')

###Test des constantes
NxConstante = 1.15
NzConstante = 0.95
PConstanteVirage=0.5
PconstanteLigneDroite=0

# attente pour qu ’ivy s’ initialise correctement
time . sleep (1.0)
IvySendMsg ("NxConstante=1.15 NzConstante=0.95")
#IvySendMsg (f"Pcst p={p}")
IvyMainLoop()
IvyStop ()