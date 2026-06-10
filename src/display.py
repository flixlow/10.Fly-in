import pygame
from src.network import Edge, Node
from src.utils import Map, Hub
import json


class Displayer:
    def __init__(self, map: Map,
                 paths: list[list[tuple[Edge, Node]]]) -> None:
        self.map: Map = map
        self.paths: list[list[tuple[Edge, Node]]] = paths
        self.step: int = -1
        self.set_screen()
        self.set_padding(0.05)
        self.set_max_coordinates()
        self.set_scales()
        self.set_origin()
        self.set_colors()
        self.set_size()
        self.set_drone_icon()

    """Visualiser for a parsed `Map` and computed paths.

    Parameters
    ----------
    map : Map
        Parsed map object containing hubs and connections.
    paths : list of list of (Edge, Node)
        Time-expanded paths for each drone to be visualised.
    """

    def set_screen(self) -> None:
        """Initialise Pygame and create the drawing surface.

        Sets `self.width`, `self.height` and `self.screen` based on the
        current display resolution.
        """
        pygame.init()
        pygame.display.set_caption("")

        self.width = pygame.display.Info().current_w * (3 / 4)
        self.height = pygame.display.Info().current_h * (3 / 4)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_padding(self, padding: float) -> None:
        """Configure drawing paddings as a fraction of the screen size.

        Parameters
        ----------
        padding : float
            Fractional padding to apply on both axes.
        """
        self.width_padding: float = self.width * padding
        self.height_padding: float = self.height * padding

    def set_max_coordinates(self) -> None:
        """Compute min/max coordinates and ranges from `map.hubs`.

        These values are later used to compute the scale and screen
        origin for plotting hub positions.
        """
        self.max_x = max([hub.x for hub in self.map.hubs])
        self.min_x = min([hub.x for hub in self.map.hubs])
        self.max_y = max([hub.y for hub in self.map.hubs])
        self.min_y = min([hub.y for hub in self.map.hubs])

        self.x_max_range = self.max_x - self.min_x
        self.y_max_range = self.max_y - self.min_y

    def set_scales(self) -> None:
        """Compute drawing scales from the coordinate ranges.

        The scale is clamped to avoid extremely large hub markers and to
        ensure the map fits the available drawing area.
        """
        self.usable_width = self.width - (self.width_padding * 2)
        self.usable_height = self.height - (self.height_padding * 2)

        max_range = max(self.x_max_range, self.y_max_range)
        self.scale: float = min(
            500,
            max(self.usable_width / max_range, self.usable_height / max_range)
        )

    def set_origin(self) -> None:
        """Compute pixel origin so the map is centred on screen."""
        center_x = (self.min_x + self.max_x) / 2
        center_y = (self.min_y + self.max_y) / 2
        self.x_center: float = self.width / 2 - (self.scale * center_x)
        self.y_center: float = self.height / 2 - (self.scale * center_y)

    def set_colors(self) -> None:
        """Load colour themes and initialise text rendering.

        Falls back to a default theme if the theme file cannot be read.
        """
        try:
            with open("assets/themes.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = [{
                "back": [236, 239, 244],
                "line": [94, 129, 172],
                "text": [46, 52, 64]
            }]
        self.themes = data
        self.current_theme = 0
        font_size = max(10, int(self.height * 0.05))
        self.font = pygame.font.Font("assets/Tanker-Regular.otf", font_size)

        self.back_color: tuple[int, int, int] = self.themes[0]["back"]
        self.line_color: tuple[int, int, int] = self.themes[0]["line"]
        self.text_color: tuple[int, int, int] = self.themes[0]["text"]

    def set_size(self) -> None:
        """Compute element sizes derived from the current scale."""
        self.line_width = max(1, int(self.scale * 0.05))
        self.outside_hub = max(1, int(self.scale * 0.1))
        self.inside_hub = self.outside_hub - self.outside_hub // 3

    def set_drone_icon(self) -> None:
        """Load and scale the drone icon used to represent drones.

        The icon is scaled according to `self.scale` and a cached
        half-size value is stored for centering during blitting.
        """
        drone_icon = pygame.image.load("assets/drone_icon.png").convert_alpha()
        icon_size = max(12, min(int(self.scale * 0.3), 120))
        size_tuple = (icon_size, icon_size)
        self.drone_icon = pygame.transform.scale(drone_icon, size_tuple)
        self.drone_icon_half = icon_size // 2

    def change_theme(self) -> None:
        """Cycle to the next available colour theme.

        Wraps back to the first theme when the end of the list is
        reached and updates the cached colour attributes.
        """
        self.current_theme += 1

        if self.current_theme >= len(self.themes):
            self.current_theme = 0

        theme = self.themes[self.current_theme]

        self.back_color = theme["back"]
        self.line_color = theme["line"]
        self.text_color = theme["text"]

    def display_connections(self) -> None:
        """Draw all static connections between hubs as lines."""
        for con in self.map.connections:
            start_hub = (
                (self.x_center + self.scale * con.start.x),
                (self.y_center + self.scale * con.start.y)
            )
            end_hub = (
                (self.x_center + self.scale * con.end.x),
                (self.y_center + self.scale * con.end.y)
            )
            pygame.draw.line(
                self.screen,
                self.line_color,
                start_hub,
                end_hub,
                self.line_width,
            )

    def display_hubs(self) -> None:
        """Draw hub markers on the screen.

        A halo (outside_hub) is drawn with the line colour and an inner
        circle is painted with the hub's configured colour.
        """
        for hub in self.map.hubs:
            x = self.x_center + self.scale * hub.x
            y = self.y_center + self.scale * hub.y
            if hub.color is not None:
                color = hub.color.value
            pygame.draw.circle(self.screen, self.line_color, (x, y),
                               self.outside_hub)
            pygame.draw.circle(self.screen, color, (x, y), self.inside_hub)

    def get_hub(self, path: list[tuple[Edge, Node]]) -> Hub:
        """Return the hub currently occupied on `path` for `self.step`.

        The method handles the special initial step (-1) and steps beyond
        the end of a path by returning the map start or the path's last
        hub respectively.
        """
        if self.step == -1:
            if self.map.start:
                return self.map.start

        if self.step >= len(path):
            return path[-1][1].real_hub

        return path[self.step][1].real_hub

    def display_drones(self) -> None:
        """Draw drone icons at the current hub for each path."""
        for path in self.paths:
            hub = self.get_hub(path)
            x = self.x_center + self.scale * hub.x
            y = self.y_center + self.scale * hub.y
            hx = x - self.drone_icon_half
            hy = y - self.drone_icon_half
            self.screen.blit(self.drone_icon, (hx, hy))

    def display_text(self) -> None:
        """Render informational text such as map name and current step."""
        text = self.font.render(
            f"Fly-in: {self.map.name}", True, self.text_color
        )
        step = self.font.render(
            f"{self.step + 1}/{self.max_path_len}", True, self.text_color
        )
        self.screen.blit(text, (
            int(self.width_padding // 2),
            int(self.height_padding // 2)
        ))
        self.screen.blit(step, (
            int(self.width - self.width_padding * 2),
            int(self.height - self.height_padding * 2)
        ))

    def display(self) -> None:
        """Main interactive display loop.

        Handles user input for stepping through time and theme changes
        and orchestrates the drawing of map elements each frame.
        """
        clock = pygame.time.Clock()
        running = True
        self.max_path_len = max((len(path) for path in self.paths), default=0)
        while running:
            self.screen.fill(self.back_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        self.change_theme()
                    if event.key == pygame.K_RIGHT:
                        if self.step < (self.max_path_len - 1):
                            self.step += 1
                    if event.key == pygame.K_LEFT:
                        if self.step > -1:
                            self.step -= 1

            self.display_connections()
            self.display_hubs()
            self.display_text()
            self.display_drones()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
