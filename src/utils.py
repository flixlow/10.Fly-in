from pydantic import BaseModel, Field
from pathlib import Path
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
    LIME = "lime"


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub(BaseModel):
    name: str
    x: int
    y: int
    zone: Zone = Field(default=Zone.NORMAL)
    color: Color = Field(default=Color.GRAY)
    max_drones: int = Field(default=1)
    connections: list['Connection'] = Field(default=[])

    def __hash__(self) -> int:
        """Get hash based on node name for use in sets and dicts.

        Returns:
            Hash value of the node's name.
        """
        return hash(self.name)


class Start(Hub):
    ...


class End(Hub):
    ...


class Connection(BaseModel):
    name: str
    start: Hub
    end: Hub
    max_link_capacity: int = Field(default=1)

    def __hash__(self) -> int:
        """Get hash based on node name for use in sets and dicts.

        Returns:
            Hash value of the node's name.
        """
        return hash(self.name)


class Map:
    def __init__(self, name: str) -> None:
        self.name = Path(name).stem.replace('_', ' ')
        self.nb_drones: int = 0
        self.hubs: list[Hub] = []
        self.start: Start | None = None
        self.end: End | None = None
        self.connections: list[Connection] = []

    def coordinate_translation(self) -> None:
        min_x = min([hub.x for hub in self.hubs])
        min_y = min([hub.y for hub in self.hubs])
        if min_x < 0:
            for hub in self.hubs:
                hub.x = hub.x - min_x
        if min_y < 0:
            for hub in self.hubs:
                hub.y = hub.y - min_y
