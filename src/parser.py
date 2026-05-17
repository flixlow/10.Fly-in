from pydantic import BaseModel, Field
from re import Pattern
from typing import Any
import re


class Drone:
    pass


class Hub(BaseModel):
    name: str = Field()
    x: int
    y: int
    flag: bool | None = Field(default=None)
    metadata: str | None = Field(default=None)

    # def model_post_init(self):
    # checker les metadatas
    # All metadata is optional and enclosed in brackets [...]
    # with default values:
    # zone=<type> (default: normal)
    # color=<value> (default: none)
    # max_drones=<number> (default: 1) -
    # Maximum drones that can occupy this
    # zone simultaneously
    # Tags inside brackets can appear in any order.
    # pass


class Connection(BaseModel):
    start: Hub
    end: Hub
    max_link_capacity: int | None = Field(default=None)


class Map:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []

    def is_valid(self) -> None:
        ...
        # if self.start_hub is not None:
        # raise Exception("More than one start hub in input file.")
        # if self.end_hub is not None:
        # raise Exception("More than one end hub in input file.")
        # for connection in self.map.connections:
        # if (connection.start == start and connection.end == end)\
        # or (connection.start == end and connection.end == start):
        # raise ValueError(f"duplicated connections: {start}-{end}.")


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

    def create_hub(self, line: str, flag: bool | None = None) -> None:
        tab = self.hub.fullmatch(line)
        if not tab:
            raise ValueError(f"Line doesn't match expected format: {line}.")
        hub = {"name": tab.group(1), "x": tab.group(2), "y": tab.group(3)}
        if flag is not None:
            hub["flag"] = flag
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

    def nb_drones(self, value: str) -> None:
        if self.first_line is True:
            raise ValueError("First line must begin with 'nb_drones'.")
        try:
            self.map.nb_drones = int(value)
            if self.map.nb_drones <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("nb_drones must be a positive integer.")
