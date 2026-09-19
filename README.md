# Mars Rover Kata

Solution Python au kata **Mars Rover** de NASA : un ensemble de rovers robotiques doit explorer un plateau rectangulaire sur Mars, en suivant des instructions de déplacement.

## Description du problème

Un rover est défini par :
- Une position `(x, y)` sur une grille
- Une direction cardinale : `N`, `S`, `E` ou `W`

Les instructions envoyées à un rover sont une chaîne de caractères composée de :
- `L` : tourner de 90° à gauche (sans se déplacer)
- `R` : tourner de 90° à droite (sans se déplacer)
- `M` : avancer d'une case dans la direction actuelle

Les rovers sont traités **séquentiellement** : le rover suivant ne bouge qu'une fois que le précédent a terminé toutes ses instructions.

## Format du fichier d'entrée

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

- La première ligne donne les coordonnées du coin supérieur droit du plateau (le coin inférieur gauche est toujours `0 0`).
- Chaque rover est décrit par deux lignes : sa position/direction de départ, puis sa chaîne d'instructions.

## Exécution

```bash
python3 rover.py input.txt
```

### Exemple de sortie

```
1 3 N
5 1 E
```

## Structure du projet

```
Mars-Rover-challenge/
├── README.md
├── rover.py       # Solution complète (parsing + simulation)
└── input.txt      # Exemple de fichier d'entrée
```

## Comportement aux limites

Si une instruction `M` ferait sortir un rover du plateau, le déplacement est simplement ignoré : le rover reste sur sa case actuelle (l'énoncé ne précisant pas ce cas, ce choix a été fait pour éviter tout comportement indéfini).