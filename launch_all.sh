#!/bin/bash

DIRECTORY="./mini_manche/src" # Dossier où se situe les fichiers python à lancer (depuis le dossier où se situe le bash).


for FICHIER in $DIRECTORY/*.py
do
	python3 $FICHIER &
done

echo "Pour quitter l'application appuyer sur q"
while true
do 
	read var
	if [[ $var == "q" ]]
	then
		break
	fi
done

pkill python3
