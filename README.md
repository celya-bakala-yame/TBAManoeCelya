# TBA

Ce dépôt contient un jeu d’aventure textuel en Python, se déroulant dans une bibliothèque universitaire mystérieuse.
Le joueur explore différents lieux, interagit avec des personnages, collecte des objets et résout des énigmes afin de découvrir les secrets cachés de la bibliothèque.

Le jeu propose un système de quêtes, des personnages non joueurs (PNJ), des objets à récupérer, ainsi que des zones secrètes accessibles à l’aide de clés.

## Guide utilisateur : 
  ***1) Comment installer le jeu ?***

git clone https://github.com/celya-bakala-yame/TBAManoeCelya.git
cd TBAManoeCelya
python game.py

  ***2) Description du jeu***
  
Vous incarnez un étudiant explorant une bibliothèque universitaire ancienne et mystérieuse.
Votre mission principale est de retrouver un livre rare caché dans les archives, tout en découvrant les secrets enfouis dans les différentes salles.

Pour progresser, vous devrez :

Explorer les différentes pièces

Résoudre des énigmes

Récupérer des objets essentiels

Parler aux personnages non joueurs

Trouver des clés pour débloquer des passages secrets

Compléter des quêtes afin de remporter la partie

L’aventure se déroule dans plusieurs lieux, notamment :

Hall

Salle de lecture

Salles de travail

Bureau du bibliothécaire

Passage secret

Salle des archives


  ***3) Comment y jouer ?***

Le jeu se joue au clavier en mode texte.

## Structuration

Le projet est structuré autour de plusieurs modules :

game.py / Game
➜ Gestion du jeu, boucle principale, interface joueur

room.py / Room
➜ Gestion des salles, sorties, portes et tiroirs

player.py / Player
➜ Gestion du joueur, inventaire, historique, quêtes

command.py / Command
➜ Gestion des commandes saisies

actions.py / Actions
➜ Implémentation des actions du joueur

item.py / Item
➜ Objets manipulables

character.py / Character
➜ Personnages non joueurs (PNJ)

quest.py / Quest & QuestManager
➜ Système de quêtes et progression

## Objectif du jeu

Le joueur gagne la partie lorsqu’il a complété toutes les quêtes principales, et perd s’il entre dans certaines zones dangereuses sans l’équipement requis.