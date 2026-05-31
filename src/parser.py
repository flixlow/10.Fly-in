import re
from typing import Any
from re import Pattern
from src.utils import Map, Hub, Connection, Start, End, Zone, Color
from src.error import MapError, HubError, ConnectionError, MetadataError


class Parser:
    def __init__(self, file: str) -> None:
        self.lines: list[str] = self.open(file)
        self.hub_pattern: Pattern[str] = re.compile(
            r"^\s+(\w+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[([^\]]+)\])?$")
        self.connection_pattern: Pattern[str] = re.compile(
            r"^\s+(\w+)-(\w+)(?:\s+\[max_link_capacity=(\d+)\])?$")
        self.names: list[str] = []
        self.coordinates: list[tuple[int, int]] = []
        self.connections: list[set[str]] = []
        self.first_line: bool = False
        self.start_hub: bool = False
        self.end_hub: bool = False
        self.map: Map = Map(file)

    def open(self, file: str) -> list[str]:
        try:
            with open(file) as f:
                return f.read().splitlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File: {file} not found.")
        except PermissionError:
            raise PermissionError(f"File: {file} permission denied.")
        except IsADirectoryError:
            raise IsADirectoryError(f"{file} is a directory.")

    def validate(self) -> Map:
        for i, line in enumerate(self.lines, start=1):
            if line == "" or line.startswith('#'):
                continue
            try:
                self.check_line(line)
            except Exception as e:
                raise type(e)(f"{str(e)}\nLine {i}: {line}")
            if not self.first_line:
                self.first_line = True
        if self.start_hub is False or self.end_hub is False:
            raise MapError("Map is missing start or end hub.")
        # self.map.coordinate_translation()
        return self.map

    def check_line(self, line: str) -> None:
        if '#' in line:
            line = line.split('#')[0]
        if line.startswith("nb_drones:"):
            self.check_nb_drones(line.removeprefix("nb_drones:"))
        elif line.startswith("start_hub:"):
            self.create_hub(line.removeprefix("start_hub:"), Start)
        elif line.startswith("hub:"):
            self.create_hub(line.removeprefix("hub:"), Hub)
        elif line.startswith("end_hub:"):
            self.create_hub(line.removeprefix("end_hub:"), End)
        elif line.startswith("connection:"):
            self.create_connection(line.removeprefix("connection:"))
        else:
            raise MapError("Unknown line type.")

    def create_hub(self, line: str, hub: type) -> None:
        if self.first_line is False:
            raise ValueError("First line must begin with 'nb_drones'.")
        tab = self.hub_pattern.fullmatch(line)
        if not tab:
            format = "<start_hub|hub|end_hub>: <name> <x> <y> [metadata]"
            raise HubError(f"Line doesn't match expected format: {format}")

        name, x, y, metadata = tab.groups()
        if name in self.names:
            raise HubError(f"Duplicated hub name: {name}")
        self.names.append(name)

        if (x, y) in self.coordinates:
            raise HubError(f"Duplicated hub coordinates: {name} ({x}, {y})")
        self.coordinates.append((int(x), int(y)))

        data_hub: dict[str, Any] = {"name": name, "x": x, "y": y}
        if metadata:
            data_hub.update(self.check_metadata(metadata))
        if hub in (Start, End):
            self.check_start_and_end(name, hub is Start)
            data_hub["max_drones"] = self.map.nb_drones
        new = hub(**data_hub)
        if isinstance(new, Start):
            self.map.start = new
        elif isinstance(new, End):
            self.map.end = new
        self.map.hubs.append(new)

    def create_connection(self, line: str) -> None:
        if self.first_line is False:
            raise ValueError("First line must begin with 'nb_drones'.")
        tab = self.connection_pattern.fullmatch(line)
        if not tab:
            format = "connection: <name1>-<name2> [metadata]"
            raise ConnectionError(f"Line doesn't match regex format: {format}")
        start, end, metadata = tab.groups()
        self.check_connection(start, end)
        for hub in self.map.hubs:
            if start == hub.name:
                start_hub = hub
            elif end == hub.name:
                end_hub = hub
        connection: dict[str, Any] = {"start": start_hub, "end": end_hub}
        if metadata:
            metadata = int(metadata)
            if metadata == 0:
                raise ConnectionError("'max_link_capacity' must be positive.")
            connection["max_link_capacity"] = metadata
        new = Connection(**connection)
        new.start.connections.append(new)
        new.end.connections.append(new)
        self.map.connections.append(Connection(**connection))

    def check_metadata(self, metadata: str) -> dict[str, Any]:
        multiple_declaration: list[str] = []
        ret: dict[str, Any] = {}
        for item in metadata.split():
            if '=' not in item:
                raise ValueError(f"Invalid metadata: {item}.")
            key, value = item.split("=", 1)
            if key in multiple_declaration:
                raise MetadataError(f"multiple declarations for {key}.")
            ret.update(self.check_one_data(key, value))
            multiple_declaration.append(key)
        return ret

    def check_connection(self, start: str, end: str) -> None:
        start_end: set[str] = {start, end}
        hubs_name = [hub.name for hub in self.map.hubs]
        if start not in hubs_name or end not in hubs_name:
            raise ConnectionError(f"Unknown hub: {start_end}")
        if start == end:
            raise ConnectionError("Hubs must be different.")
        if start_end in self.connections:
            raise ConnectionError(f"Duplicated connections: {start_end}")
        else:
            self.connections.append(start_end)

    def check_start_and_end(self, name: str, position: bool) -> None:
        if position and self.start_hub:
            raise MapError(f"Duplicated start_hub: {name}")
        elif position and not self.start_hub:
            self.start_hub = True
        if not position and self.end_hub:
            raise MapError(f"Duplicated end_hub: {name}")
        elif not position and not self.end_hub:
            self.end_hub = True

    def check_one_data(self, key: str, value: str) -> dict[str, Any]:
        if value == '':
            raise MetadataError(f"Empty metadata input for {key}.")
        match key:
            case "zone":
                try:
                    return ({"zone": Zone(value)})
                except ValueError:
                    raise MetadataError(f"'{value}' is not a valid zone type.")
            case "color":
                try:
                    return ({"color": Color(value.lower())})
                except ValueError:
                    print("\033[1;38;5;208m[WARNING]\033[0m",
                          f" '{value}' color is not a known color.")
                    return ({"color": Color.GRAY})
            case "max_drones":
                try:
                    ret = int(value)
                    if ret <= 0:
                        raise ValueError
                    return ({"max_drones": ret})
                except ValueError:
                    raise MetadataError(
                        f"max_drones must be a positive integer: '{value}'.")
            case _:
                raise MetadataError(f"Unknown key for metadata: '{key}'.")

    def check_nb_drones(self, value: str) -> None:
        if self.first_line is True:
            raise ValueError("First line must begin with 'nb_drones'.")
        try:
            self.map.nb_drones = int(value)
            if self.map.nb_drones <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("nb_drones must be a positive integer.")
