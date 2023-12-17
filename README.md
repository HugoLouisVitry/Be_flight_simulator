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
- `^FCUAP1 on`

A destination du FGS : 
+ `MancheFlap f=(\S+)`
+ `MancheLdg ldg=(\S+)` 
Flaps : 0,1 ou 2
Landings gears : 0 rentré , 1 déployé 

# Reception :

Venant du FGS :
+ `^LimitsN nx=(\S+) nz=(\S+) nx_AP=(\S+) nz_AP=(\S+)`

Venant du PA-Long : 
+ `APLongNzControl nz=(\S+)`
+ `APLongNxControl nx=(\S+)`

Venant du PA-Lat:
+ `APLatpControl p=(\S+)`

Venant du FCU:
- `^FCUAP1 push`
- `^FCUAP1 off`
- `^FCUAP1 on`

# Messages interne :
+ `MancheCmdAxe nz=(\S+) p=(\S+)`
+ `MancheAP push`
+ `MancheCmdPoussee dnx=(\S+)`
+ `MancheThr auto_thr=(\S+)`


# Utilisation 
Pour utiliser le module du mini manche, lancer les deux fichiers contenu dans le dossier src. L'un gère le joystick, l'autre la commande. La commande fonctionne sans le joystick mais le joystick n'influence pas le modèle avion sans la commande.
La commande n'envoie de consignes longitudinales qu'a récéption d'un message du paLong et de même pour le paLat. Donc il faudra utiliser les modules de test ou les originaux pour tester.
La gestion des flaps et du train se fait depuis le joystick indépendament de l'état de l'auto pilote.
