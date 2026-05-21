*This project has been created as part of the 42 curriculum by flauweri.*

# Description

# Instructions

# Resources

## IA
- learning how to use Regex for parsing

## doc
- https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124 color ansi
- https://regex101.com/ regex checker
- https://regex-generator.olafneumann.org/ regex generator


# Algorithm choices and implementation strategy

# Visual representation features

Parser:
flauweri
[x]supprimer commentaires et lignes vides
[x]chercher premiere ligne nb drones
[x]checker le regex pour chaque ligne entre celui des hubs et celui des connexions
[x]ensuite creer les objets hub et connexion
[x]gerer les metadatas
[x]transformer en dict cle valeur
[x]verifier les clés valeur
[x]plusieurs meme metadata dans les []
[x]changer le bool | None par l Enum
[x]les ajouter a la map
[x]verifier que la map est coherente (connexion sans duplication, un seul start, un seul end)
[x]verifier les noms des hub qui ne doivent pas etre dupliqué

bcondemi
[x]color multiple declaration
[x]gray issue default
[x]same thing for zone
[x]max drones for start and end can't be inferior to nb_drones
    end_hub: goal 3 0 [color=red max_drones=0]
    nb_drones: 2
[x]check if start and end for connection exists or not
    connection: start-waypoint1
    start_hub: start 0 0 [color=green]
    hub: waypoint1 1 0 [color=blue]
    hub: waypoint2 2 0 [color=blue]
    connection: waypoint2-goal [max_link_capacity=2 max_link_capacity=2]

    connection: startewgwgq-waypoint1
    [ERROR] cannot access local variable 'start_hub' where it is not associated with a value
    if start_hub is None or end_hub is None:
        raise ConnectionError(f"Unknown hub for connection: {line}.")
    connection: dict[str, Any] = {"start": start_hub, "end": end_hub}
[x]multiple declaration on metadata for connection

lgirard
[x] raise MapError with description
[x] Line doesn't match expected format. add format
[x] position: bool | None = None :)
[x] Start must be different from end. il n'y a pas de start ou de end dans les connections
[x] if line == "" or line.startswith('#'): Les commentaires peuvent etre dans une ligne
[x] Utiliser argparse
[x] Verifier presence de end_hub et start_hub

debug: 
    # for hub in map.hubs:
    #     if isinstance(hub, Start):
    #         print("\033[1;36m[START HUB]\033[0m:", hub)
    #     elif isinstance(hub, End):
    #         print("\033[1;36m[END HUB]\033[0m:", hub)
    #     else:
    #         print("\033[1;34m[HUB]\033[0m:", hub)
    # for con in map.connections:
    #     print("\033[1;35m[CONNECTION]\033[0m:", con.start.name, end=" ")
    #     print(con.end.name, con.max_link_capacity)

displayer:
degradé de fond vibe codé
    # def shade(self, factor: float) -> tuple[int, int, int]:
    #     color = self.back_color
    #     return (
    #         max(0, min(int(color[0] * factor), 255)),
    #         max(0, min(int(color[1] * factor), 255)),
    #         max(0, min(int(color[2] * factor), 255))
    #     )

    # def draw_gradient(self) -> None:
    #     bottom = self.shade(0.4)
    #     top = self.shade(1.5)
    #     for y in range(round(self.height)):
    #         ratio = y / self.height

    #         r = top[0] * (1 - ratio) + bottom[0] * ratio
    #         g = top[1] * (1 - ratio) + bottom[1] * ratio
    #         b = top[2] * (1 - ratio) + bottom[2] * ratio

    #         pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))

    [ ] probleme affichage sur maze nightmare
    [ ] est ce que le make import c est une bonne idee ?
    [ ] self.map.coordinate_translation() shoulds i use this
    [ ] 
algo:
