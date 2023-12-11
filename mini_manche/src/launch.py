import subprocess
import time

files_path = ['commande.py','manche.py']
procs = []

for file in files_path :
    procs.append(subprocess.Popen(['python3', file]))


time.sleep(3)
print("Entrez q pour sortir du programme")
x = ''
while x != "q":
    x = input()

for proc in procs:
    proc.kill()
