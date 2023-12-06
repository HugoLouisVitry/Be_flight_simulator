import ivy.std_api as ivy
import time
from ivy.std_api import *

### Ivy Bus
def on_cx_proc (agent , connected ) :
    pass
def on_die_proc (agent , _id ):
    pass
def on_time(agent, *larg):
    IvySendMsg("PConstanteVirage=0.5 PConstanteLigneDroite=0")
    IvySendMsg ("NxConstante=1.15 NzConstante=0.95")
    
app_name = "Minimanchetestpa"
ivy_bus = "127.255.255.255:2010"
IvyInit ( app_name , # application name for Ivy
"[%s ready ]" % app_name , # ready message
0, # main loop is local
on_cx_proc , # called on cx/ disconnect
on_die_proc ) # called when the agent dies
IvyStart ( ivy_bus )
IvyBindMsg(on_time, '^Time t=(.*)')





PConstanteVirage=0.5
PConstanteLigneDroite=0
NxConstante = 1.15
NzConstante = 0.95


### Envoie message Ivy

def null_cb (*a):
    pass

# attente pour qu ’ivy s’ initialise correctement
time . sleep (1.0)
IvySendMsg ("PConstanteVirage=0.5 PConstanteLigneDroite=0")
IvySendMsg ("NxConstante=1.15 NzConstante=0.95")
IvyMainLoop()
IvyStop ()


