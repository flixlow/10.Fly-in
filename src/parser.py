from pydantic import BaseModel, Field
from re import Pattern
from typing import Any
from enum import Enum
import re


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"
    BLACK = "black"
    YELLOW = "yellow"
    GRAY = "gray"
    CYAN = "cyan"
    MAGENTA = "magenta"
    ORANGE = "orange"
    PURPLE = "purple"


class MapError(Exception):
    ...


class MetadataError(Exception):
    def __init__(
            self,
            message: str = "zone=<type>, color=<value>, max_drones=<number>"
            ) -> None:
        super().__init__(message)


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub(BaseModel):
    name: str = Field()
    x: int
    y: int
    position: bool | None = Field(default=None)
    zone: str | None = Field(default=None)
    color: Color | None = Field(default=None)
    max_drones: int | None = Field(default=None)


class Connection(BaseModel):
    start: Hub
    end: Hub
    max_link_capacity: int | None = Field(default=None)


class Map:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []

    def check_start_and_end(self) -> None:
        n_start = 0
        n_end = 0
        for hub in self.hubs:
            if hub.position is None:
                continue
            if hub.position is True:
                n_start += 1
            if hub.position is False:
                n_end += 1
        if n_start != 1 or n_end != 1:
            raise MapError("Map should contain exaclty one start and one end.")

    def check_connection(self) -> None:
        for i in self.connections:
            for j in self.connections:
                if ((i.start, i.end) == (j.start, j.end) or (i.start, i.end) == (j.end, j.start)):
                    raise ValueError(
                        f"duplicated connections: {i.start}-{i.end}.")

    def is_valid(self) -> None:
        self.check_start_and_end()
        self.check_connection()


class Parser:
    def __init__(self, file: str) -> None:
        self.file: str = file
        self.lines: list[str]
        self.map = Map()
        self.hub: Pattern = re.compile(
            r"^\s+(\w+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[([^\]]+)\])?$")
        self.connection: Pattern = re.compile(
            r"^\s+(\w+)-(\w+)(?:\s+\[max_link_capacity=(\d+)\])?$")
        self.first_line: bool = False
        self.start_hub: bool = False
        self.end_hub: bool = False

    def validate_and_parse(self) -> Map:
        self.open()
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

    def open(self) -> None:
        try:
            with open(self.file) as f:
                self.lines = f.read().split("\n")
        except FileNotFoundError:
            raise FileNotFoundError(f"File: {self.file} not found.")
        except PermissionError:
            raise PermissionError(f"File: {self.file} permission denied.")
        except IsADirectoryError:
            raise IsADirectoryError(f"{self.file} is a directory.")

    def create_hub(self, line: str, position: bool | None = None) -> None:
        tab = self.hub.fullmatch(line)
        if not tab:
            raise ValueError(f"Line doesn't match expected format: {line}.")
        name, x, y, metadata = tab.groups()
        hub: dict[str, Any] = {"name": name, "x": x, "y": y}
        if position is not None:
            hub["position"] = position
        if metadata:
            processed: dict[str, str | int] = {}
            for item in metadata.split():
                if '=' not in item:
                    raise ValueError(f"Invalid metadata: {item}.")
                key, value = item.split("=", 1)
                processed[key] = value
            hub.update(self.validate_metadata(processed))
        self.map.hubs.append(Hub(**hub))

    def create_connection(self, line: str) -> None:
        tab = self.connection.fullmatch(line)
        if not tab:
            raise ValueError(f"Line doesn't match expected format: {line}.")
        for hub in self.map.hubs:
            if tab.group(1) == hub.name:
                start = hub
            elif tab.group(2) == hub.name:
                end = hub
        if start is None or end is None:
            raise ValueError(f"Unknown hub for connection: {line}")
        connection: dict[str, Any] = {"start": start, "end": end}
        if tab.group(3):
            connection["max_link_capacity"] = tab.group(3)
        self.map.connections.append(Connection(**connection))

    def validate_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        formated: dict[str, Any] = {}
        for k, v in metadata.items():
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
                        if v < 0:
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
