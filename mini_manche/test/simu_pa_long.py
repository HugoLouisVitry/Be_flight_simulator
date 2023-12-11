import time
from ivy.std_api import *

### Ivy Bus
def on_cx_proc (agent , connected ) :
    pass
def on_die_proc (agent , _id ):
    pass
def on_time(agent, *larg):
    if float(larg[0]) < 10:
        nx=3
        nz=3
    elif 20<float(larg[0])<30:
        nx=0.001
        nz=0.001
    else: 
        nx, nz= 1,1
    
    IvySendMsg(f"APLongNxControl nx={1}")
    IvySendMsg(f"APLongNzControl nz={1}")


   

app_name = "Minimanchetestlongi"
ivy_bus = "127.255.255.255:2010"
IvyInit ( app_name , # application name for Ivy
"[%s ready ]" % app_name , # ready message
0, # main loop is local
on_cx_proc , # called on cx/ disconnect
on_die_proc ) # called when the agent dies
IvyStart ( ivy_bus )
IvyBindMsg(on_time, '^Time t=(\S+)')



# attente pour qu ’ivy s’ initialise correctement
time . sleep (1.0)

