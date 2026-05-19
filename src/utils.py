from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


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
    BROWN = "brown"
    MARRON = "maroon"
    GOLD = "gold"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub(BaseModel):
    name: str = Field()
    x: int
    y: int
    zone: Optional[Zone] = Field(default=Zone.NORMAL)
    color: Optional[Color] = Field(default=Color.GRAY)
    max_drones: Optional[int] = Field(default=1)


class Start(Hub):
    ...


class End(Hub):
    ...


class Connection(BaseModel):
    start: Hub
    end: Hub
    max_link_capacity: int | None = Field(default=None)


class Map:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []
