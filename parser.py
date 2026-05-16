from pydantic import BaseModel, Field


class Drone:
    pass


class Hub(BaseModel):
    name: str = Field()
    x: int
    y: int


class Connection:
    def __init__(self, name: str) -> None:
        self.name = name


class Maps:
    def __init__(self) -> None:
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None

    def is_valid(self) -> None:
        ...


class Parser:
    def __init__(self, file: str) -> None:
        self.file: str = file
        self.lines: list[str]
        self.number_of_drones: int = 0
        self.map = Maps()

    def create_hub(self, line: str, flag: bool = None) -> None:
        tab = line.split()
        if len(tab) == 3:
            if flag is None:
                self.map.hubs.append(Hub(tab[0], tab[1], tab[2]))
            if flag is True:
                if self.map.start_hub is not None:
                    raise Exception("more than one start hub in input file.")
                self.map.start_hub = Hub(tab[0], tab[1], tab[2])
            if flag is False:
                if self.map.end_hub is not None:
                    raise Exception("more than one end hub in input file.")
                self.map.end_hub = Hub(tab[0], tab[1], tab[2])
        if len(tab) == 4:
            if flag is None:
                self.map.hubs.append(Hub(tab[0], tab[1], tab[2], tab[3]))
        else:
            raise Exception(f"invalid number of argument: {line}")

    def create_connexion(self, line: str) -> None:
        print(line)

    def validate_nb_drones(self) -> None:
        if not self.lines[0] or not self.lines[0].startswith("nb_drones: "):
            raise Exception("ca doit commencer avec nb_drones")
        else:
            try:
                int(self.lines[0].removeprefix("nb_drones: "))
            except Exception:
                raise Exception("c'est pas un chiffre ça") from None

    def remove_comments(self) -> None:
        new: list[str] = []
        for i in range(len(self.lines)):
            if self.lines[i].startswith('#') or self.lines[i] == '':
                continue
            else:
                new.append(self.lines[i])
        self.lines = new

    def validate(self) -> None:
        self.remove_comments()
        self.validate_nb_drones()
        for line in self.lines[1:]:
            match line.split(':')[0]:
                case "start_hub":
                    self.create_hub(line.removeprefix("start_hub: "), True)
                case "end_hub":
                    self.create_hub(line.removeprefix("end_hub: "), False)
                case "hub":
                    self.create_hub(line.removeprefix("hub: "))
                case "connection":
                    self.create_connexion(line.removeprefix("connection: "))
                case _:
                    raise Exception("not hub ou connection line begin with")

    def open(self) -> None:
        try:
            with open(self.file) as f:
                self.lines = f.read().split("\n")
        except FileNotFoundError:
            raise FileNotFoundError(f"File: {self.file} not found.") from None
        except PermissionError:
            raise FileNotFoundError(
                f"File: {self.file} permission denied.") from None
        except Exception:
            raise Exception("Error appends during parsing.")
        else:
            self.validate()
