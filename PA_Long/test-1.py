from ivy.std_api import *
import time
import numpy as np

def op(agent, connected):
    pass
def cl(agent, _id):
    pass

app_n ="PAlong"
ivy_bus ="127.255.255.255:2017"
IvyInit(app_n ,"ready" ,0 ,op ,cl )
IvyStart(ivy_bus)


time.sleep(1)
IvySendMsg("StateVector x=0 y=0 z=10000 IAS=200 fpa={} psi={} phi={}".format(np.deg2rad(0),np.deg2rad(20),np.deg2rad(0)))
time.sleep(1)
IvySendMsg("LimitsN nx_neg=-1 nx_pos=2.5 nz_neg=-1 nz_pos=2.5")
time.sleep(1)
IvySendMsg("SpeedLimits vmin=100 vmax=400")
time.sleep(1)
#IvySendMsg("FCUSpeedMach Mode=Selected Val=150") 
#time.sleep(1)
#IvySendMsg("ManagedSpeed vi=200")
time.sleep(1)
#IvySendMsg("ManagedAlt alt=5000 Q=1013")
IvySendMsg("FCUVertical Altitude=10000 Mode=FPA Val={}".format(np.deg2rad(-5)))
time.sleep(5)
#IvySendMsg("StateVector x=0 y=0 z=10000 IAS=200 fpa={} psi={} phi={}".format(np.deg2rad(-5),np.deg2rad(20),np.deg2rad(0)))
IvyStop()








