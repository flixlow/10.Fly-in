from pydantic import BaseModel, Field
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
    zone: Zone | None = Field(default=None)
    color: Color | None = Field(default=None)
    max_drones: int | None = Field(default=1)


class Connection(BaseModel):
    start: Hub
    end: Hub
    max_link_capacity: int | None = Field(default=None)


class Map:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []
