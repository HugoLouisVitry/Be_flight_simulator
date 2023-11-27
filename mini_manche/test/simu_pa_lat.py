import ivy.std_api as ivy


### Ivy Bus
app_name = " MyIvyApplication "
ivy_bus = " 127.255.255.255:2010 "
IvyInit ( app_name , # application name for Ivy
"[%s ready ]" % app_name , # ready message
0, # main loop is local
on_cx_proc , # called on cx/ disconnect
on_die_proc ) # called when the agent dies
IvyStart ( ivy_bus )

###Test des constantes
PConstanteVirage = 0.5
PconstanteLigneDroite = 0


### Envoie message Ivy
import time
from ivy . std_api import *
def null_cb (*a):
    pass
IvyInit (" IvyApp ", " Ready ", 0 , null_cb , null_cb )
IvyStart (" 127.255.255.255:2010 ")
# attente pour qu ’ivy s’ initialise correctement
time . sleep (1.0)
IvySendMsg (" PConstanteVirage = 0.5 PconstanteLigneDroite = 0  ")
IvyStop ()