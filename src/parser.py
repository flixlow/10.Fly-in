from .utils import Map, Hub, Connection, Zone, Color
from .error import MapError, HubError, ConnectionError, MetadataError
from re import Pattern
from typing import Any
import re


class Parser:
    def __init__(self, file: str) -> None:
        self.lines: list[str] = self.open(file)
        self.file: str = file
        self.names: list[str] = []
        self.connections: list[set[str]] = []
        self.coordinates: list[tuple[int, int]] = []
        self.map = Map()
        self.hub_pattern: Pattern = re.compile(
            r"^\s+(\w+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[([^\]]+)\])?$")
        self.connection_pattern: Pattern = re.compile(
            r"^\s+(\w+)-(\w+)(?:\s+\[max_link_capacity=(\d+)\])?$")
        self.first_line: bool = False
        self.start_hub: bool = False
        self.end_hub: bool = False

    def validate(self) -> Map:
        for line in self.lines:
            if line == "" or line.startswith('#'):
                continue
            elif line.startswith("nb_drones:"):
                self.nb_drones(line.removeprefix("nb_drones:"))
            elif line.startswith("start_hub:"):
                self.create_hub(line.removeprefix("start_hub:"), True)
            elif line.startswith("hub:"):
                self.create_hub(line.removeprefix("hub:"))
            elif line.startswith("end_hub:"):
                self.create_hub(line.removeprefix("end_hub:"), False)
            elif line.startswith("connection:"):
                self.create_connection(line.removeprefix("connection:"))
            else:
                raise ValueError(f"Unvalid line: {line}")
            if not self.first_line:
                self.first_line = True
        return self.map

    def open(self, file: str) -> list[str]:
        try:
            with open(file) as f:
                return f.read().splitlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File: {self.file} not found.")
        except PermissionError:
            raise PermissionError(f"File: {self.file} permission denied.")
        except IsADirectoryError:
            raise IsADirectoryError(f"{self.file} is a directory.")

    def create_hub(self, line: str, position: bool | None = None) -> None:
        tab = self.hub_pattern.fullmatch(line)
        if not tab:
            raise HubError(f"Line doesn't match expected format: {line}.")
        name, x, y, metadata = tab.groups()
        if name in self.names:
            raise HubError(f"Duplicated hub name: {name}")
        else:
            self.names.append(name)
        if (x, y) in self.coordinates:
            raise HubError(f"Duplicated hub coordinates: {name} ({x}, {y})")
        else:
            self.coordinates.append((x, y))

        hub: dict[str, Any] = {"name": name, "x": x, "y": y}
        if position is not None:
            self.check_start_and_end(name, position)
            hub["position"] = position
        if metadata:
            hub.update(self.validate_metadata(metadata))
        self.map.hubs.append(Hub(**hub))

    def check_duplicated_connection(self, start: str, end: str) -> None:
        start_end: set[str] = {start, end}
        if start_end in self.connections:
            raise ConnectionError(f"Duplicated connection: {start_end}")
        else:
            self.connections.append(start_end)

    def create_connection(self, line: str) -> None:
        tab = self.connection_pattern.fullmatch(line)
        if not tab:
            raise ConnectionError(f"Line doesn't match regex format: {line}.")
        start, end, metadata = tab.groups()
        if start == end:
            raise ConnectionError(f"Start must be different from end: {line}.")
        self.check_duplicated_connection(start, end)
        for hub in self.map.hubs:
            if start == hub.name:
                start_hub = hub
            elif end == hub.name:
                end_hub = hub
        if start_hub is None or end_hub is None:
            raise ConnectionError(f"Unknown hub for connection: {line}.")
        connection: dict[str, Any] = {"start": start_hub, "end": end_hub}
        if metadata:
            connection["max_link_capacity"] = metadata

        self.map.connections.append(Connection(**connection))

    def check_start_and_end(self, name: str, position: bool) -> None:
        if position and self.start_hub:
            raise MapError(f"Duplicated start_hub: {name}")
        elif position and not self.start_hub:
            self.start_hub = True
        if not position and self.end_hub:
            raise MapError(f"Duplicated end_hub: {name}")
        elif not position and not self.end_hub:
            self.end_hub = True

    def validate_metadata(self, metadata: str) -> dict[str, Any]:
        formated: dict[str, Any] = {}

        for item in metadata.split():
            if '=' not in item:
                raise ValueError(f"Invalid metadata: {item}.")

            k, v = item.split("=", 1)
            match k:
                case "zone":
                    for z in Zone:
                        if v == z.value:
                            formated["zone"] = z
                    if not formated.get("zone"):
                        raise MetadataError(f"Unknown zone type: {v}.")
                case "color":
                    try:
                        formated["color"] = Color[v]
                    except KeyError:
                        formated["color"] = Color("gray")
                case "max_drones":
                    try:
                        formated["max_drones"] = int(v)
                        if formated["max_drones"] < 0:
                            raise MetadataError
                    except MetadataError:
                        raise MetadataError(
                            f"max_drones must be a non negative int: {v}.")
                case _:
                    raise MetadataError

        return formated

    def nb_drones(self, value: str) -> None:
        if self.first_line is True:
            raise ValueError("First line must begin with 'nb_drones'.")
        try:
            self.map.nb_drones = int(value)
            if self.map.nb_drones <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("nb_drones must be a positive integer.")
