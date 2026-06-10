*This project has been created as part of the 42 curriculum by flauweri.*

## Description

Fly-in est un simulateur de routage de drones. L'objectif
du projet est de calculer et d'afficher des trajectoires permettant d'envoyer un nombre donné
de drones d'un hub de départ vers un hub d'arrivée en respectant des contraintes de capacité
sur les hubs et sur les liaisons, ainsi que des règles liées aux zones (normal, prioritaire,
restreinte, bloquée). Le simulateur construit un graphe dépendant du temps (time-expanded graph),
recherche des chemins d'acheminement valides puis affiche la simulation.

## Instructions

- Prérequis : Python >= 3.13, dépendances listées dans `pyproject.toml` (pygame, pydantic, questionary, ...).

- Pour installer l'environnement virtuel:

```bash
make install
```

- Pour préparer les cartes fournies :

	```bash
	make map
	```

- Pour lancer l'application (sélection interactive d'une carte) :

	```bash
	make run
	```

- Pour lancer avec un dossier spécifique :

	```bash
	make ARG="--directory nom_du_dossier"
	make ARG="--d nom_du_dossier"
	```

- Pour lancer avec une carte spécifique :

	```bash
	make ARG="--input maps/nom_de_la_carte.txt"
	make ARG="--i maps/nom_de_la_carte.txt"
	```

- Nettoyage et utilitaires :

	```bash
	make clean
	make lint
  make lint-strict
	```

## Ressources

- Algorithmes de flot : documentation et articles sur Edmonds–Karp, Dinic et flots sur réseaux (ouvrages et articles en ligne).
- Pygame : https://www.pygame.org/
- Pydantic : https://docs.pydantic.dev/

Utilisation de l'IA :
- J'ai utilisé une assistance IA pour rédiger et structurer ce fichier `README.md` ainsi que les docstrings (description, sections,
	mise en forme et explication générale des choix). Aucun code source n'a été généré ou modifié par l'IA.

## Choix d'algorithme et stratégie d'implémentation

- Représentation temporelle : le graphe est étendu dans le temps : chaque hub est instancié pour chaque pas de temps
	nécessaire. Cela permet de modéliser le déplacement des drones d'un pas de temps à l'autre et d'appliquer des
	capacités sur les hubs et les liaisons.
- Nœuds et arcs :
	- `Node` représente un hub à un instant donné ; il garde la trace des arêtes sortantes et du nombre de passages.
	- `Edge` représente une liaison (ou une attente statique) avec une capacité de lien (`max_link_capacity`).
- Recherche de chemins :
	- Une recherche en profondeur (DFS) est utilisée pour extraire des chemins augmentants dans le graphe temps-dépendant.
	- Pour chaque chemin trouvé, on calcule le flux bloquant possible en regardant les capacités restantes des arêtes
		et des nœuds (hubs) du chemin, puis on applique ce flux (incrémentation des compteurs `passage`).
	- Les arêtes sont triées pour privilégier les zones `PRIORITY` lorsqu'il y a un choix, ce qui favorise l'usage
		de hubs prioritaires pour améliorer l'expérience utilisateur ou des contraintes métier.
- Boucle d'exécution :
	- Construction progressive du réseau via `Network.next_step()` jusqu'à ce que le graphe n'évolue plus
		ou qu'un seuil de répétition soit atteint.
	- Application répétée de la collecte de chemins augmentants (`DFS.get_max_flow()`) jusqu'à atteindre
		le nombre de drones requis (`map.nb_drones`) ou épuiser les possibilités.

## Représentation visuelle et expérience utilisateur

- Échelle adaptative : l'affichage calcule automatiquement l'échelle et le centre pour que la carte
	s'adapte à la taille de la fenêtre (padding, scale, origin).
- Thèmes et couleurs : support d'un fichier `assets/themes.json` pour personnaliser les couleurs de fond,
	lignes et textes ; basculement possible entre thèmes.
- Hubs et liaisons : les hubs sont dessinés avec des tailles dépendant de l'échelle ; les liaisons sont tracées
	en lignes. Les hubs prioritaire/restricted sont représentés par des couleurs et styles différents pour
	indiquer visuellement leurs effets sur les trajectoires.
- Drones : icônes graphiques (`assets/drone_icon.png`) utilisées pour animer les drones le long des chemins trouvés.
	L'animation se fait pas à pas suivant l'horloge interne et la longueur des chemins extraits par l'algorithme.
- Texte et information : affichage du nom de la carte et autres informations utiles pendant la simulation
	(police incluse dans `assets` si disponible).

Ces éléments visuels aident l'utilisateur à comprendre :
- pourquoi certains drones prennent des chemins différents (priorité / capacité),
- où se produisent les saturations ou blocages (zones restreintes / capacités atteintes),
- l'évolution temporelle des déplacements (animation pas-à-pas).

## Exemples d'utilisation

- Simulation rapide (sélection interactive) : `python3 -m src` puis choisir une carte.
- Exécution non interactive : `python3 -m src --input maps/exemple.txt`.

## Structure du projet (brève)

- `src/parser.py` : lecture et validation des fichiers de carte (.txt) et construction de l'objet `Map`.
- `src/network.py` : construction du graphe temps-dépendant (nœuds, arêtes) et évolution par pas de temps.
- `src/algo.py` : recherche de chemins augmentants, calcul des flux et application des passages.
- `src/output.py` : génération de la sortie texte (liste de mouvements par pas) et création des objets `Drone`.
- `src/display.py` : affichage Pygame de la carte et animation des drones.

## Contribution et améliorations possibles

- Tests unitaires et validation automatique des parsers et des invariants de capacité.

---

docstring manquante au format pep257 numpy style en anglais stp