# Be_flight_simulator
Simulateur de vol inclus dans un projet d'apprentissage de l'ENAC

Pour cloner utilisez la commande : 
+ `git clone --recurse-submodules [lien]`

Si vous aviez déjà cloné le repo faites plutot : 
+ `git pull`
+ `git submodule update --init --recursive`

# Messages IVY envoyé par le mini manche :

Commande pour le modèle avion :
- `^APNxControl nx=(\S+)`
- `^APNzControl nz=(\S+)`
- `^APLatControl rollRate=(\S+)`

Commande pour le FCU:
- `^FCUAP1 push`
- `FCUAP1 off`


Message du PA-Long : 
+ `APLongNzControl nz=(\S+)`
+ `APLongNxControl nx=(\S+)`


Message du PA-Lat:
+ `APLatpControl p=(\S+)`