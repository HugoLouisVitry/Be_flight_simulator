# Be_flight_simulator
Simulateur de vol inclus dans un projet d'apprentissage de l'ENAC

Pour cloner utilisez la commande : 
+ `git clone --recurse-submodules [lien]`

Si vous aviez déjà cloné le repo faites plutot : 
+ `git pull`
+ `git submodule update --init --recursive`

## Messages ivy

# Emission :

A destination du modèle avion :
- `^APNxControl nx=(\S+)`
- `^APNzControl nz=(\S+)`
- `^APLatControl rollRate=(\S+)`

A destination du FCU:
- `^FCUAP1 push`
- `^FCUAP1 off`

A destination du FGS : 
+ `MancheFlap f=(S+)`
+ `MancheLdg ldg=(S+)` 

Pour les landings gears : 0 rentré , 1 déployé 

# Reception :

Venant du FGS :
+ `^LimitsN nx=(\S+) nz=(\S+) nx_AP=(\S+) nz_AP=(\S+)`

Venant du PA-Long : 
+ `APLongNzControl nz=(\S+)`
+ `APLongNxControl nx=(\S+)`

Venant du PA-Lat:
+ `APLatpControl p=(\S+)`