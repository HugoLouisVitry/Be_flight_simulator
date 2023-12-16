import subprocess
import time
import os

files_mini_manche = ['src/commande.py','src/manche.py'] #,'test/simu_pa_lat.py','test/simu_pa_long.py']
files_FGS = ['main.py']
files_APLong = ['PA_long.py']
files_APLat = ['module_PALat.py']
procs = []

def launch(directory,return_dir,liste):
    os.chdir(directory)
    for file in liste :
        procs.append(subprocess.Popen(['python3', file]))
    os.chdir(return_dir)

launch("mini_manche","..",files_mini_manche)
launch("FGS/min-avi-fgs","../..",files_FGS)
launch("PA_Long","..",files_APLong)
launch("PA_Lat","..",files_APLat)


time.sleep(3)
print("Entrez q pour sortir du programme")
x = ''
while x != "q":
    x = input()

for proc in procs:
    proc.kill()
