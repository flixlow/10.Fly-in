import pygame  # type: ignore
from .algo import Edge, Node
from .utils import Map, Hub
import json


class Displayer:
    def __init__(self, map: Map,
                 paths: list[list[tuple[Edge, Node]]]) -> None:
        self.map: Map = map
        self.paths: list[list[tuple[Edge, Node]]] = paths
        self.time: int = -1
        self.set_screen()
        self.set_padding(0.05)
        self.set_origin()
        self.set_max_coordinates()
        self.set_scales()
        self.set_colors()
        self.set_size()
        self.set_drone_icon()

    def set_size(self) -> None:
        self.line_width = max(1, int(self.scale * 0.05))
        self.outside_hub = max(1, int(self.scale * 0.1))
        self.inside_hub = self.outside_hub - self.outside_hub // 3

    def set_screen(self) -> None:
        pygame.init()
        pygame.display.set_caption("")

        self.width = pygame.display.Info().current_w * (3/4)
        self.height = pygame.display.Info().current_h * (3/4)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_padding(self, padding: float) -> None:
        width_padding: float = self.width * padding
        height_padding: float = self.height * padding
        self.padding = max(width_padding, height_padding)

    def set_origin(self) -> None:
        self.x_center: float = self.padding
        self.y_center: float = self.height / 2

    def set_max_coordinates(self) -> None:
        self.max_x: int = max(2, max([hub.x for hub in self.map.hubs]))
        self.max_y: int = max(2, max([hub.y for hub in self.map.hubs]))

    def set_scales(self) -> None:
        usable_width = self.width - (self.padding * 2)
        usable_height = self.height - (self.padding * 2)
        self.scale: float = min(usable_width / self.max_x,
                                usable_height / self.max_y)

    def set_colors(self) -> None:
        try:
            with open("assets/themes.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = [{"back": [236, 239, 244],
                     "line": [94, 129, 172],
                     "text": [46, 52, 64]}]
        self.themes = data
        self.current_theme = 0
        font_size = max(10, int(self.height * 0.05))
        self.font = pygame.font.Font("assets/Tanker-Regular.otf", font_size)

        self.back_color: tuple[int, int, int] = self.themes[0]["back"]
        self.line_color: tuple[int, int, int] = self.themes[0]["line"]
        self.text_color: tuple[int, int, int] = self.themes[0]["text"]

    def set_drone_icon(self) -> None:
        drone_icon = pygame.image.load("assets/drone_icon.png").convert_alpha()
        icon_size = max(12, min(int(self.scale * 0.3), 120))
        size_tuple = (icon_size, icon_size)
        self.drone_icon = pygame.transform.scale(drone_icon, size_tuple)
        self.drone_icon_half = icon_size // 2

    def change_theme(self) -> None:
        self.current_theme += 1

        if self.current_theme >= len(self.themes):
            self.current_theme = 0

        theme = self.themes[self.current_theme]

        self.back_color = theme["back"]
        self.line_color = theme["line"]
        self.text_color = theme["text"]

    def display_connections(self) -> None:
        for con in self.map.connections:
            start_hub = ((self.x_center + self.scale * con.start.x),
                         (self.y_center + self.scale * con.start.y))
            end_hub = ((self.x_center + self.scale * con.end.x),
                       (self.y_center + self.scale * con.end.y))
            pygame.draw.line(self.screen, self.line_color,
                             start_hub, end_hub, self.line_width)

    def display_hubs(self) -> None:
        for hub in self.map.hubs:
            x = self.x_center + self.scale * hub.x
            y = self.y_center + self.scale * hub.y
            if hub.color is not None:
                color = hub.color.value
            pygame.draw.circle(self.screen, self.line_color,
                               (x, y), self.outside_hub)
            pygame.draw.circle(self.screen, color, (x, y), self.inside_hub)

    def get_hub(self, path: list[tuple[Edge, Node]]) -> Hub:
        if self.time == -1:
            if self.map.start:
                return self.map.start

        if self.time >= len(path):
            return path[-1][1].real_hub

        return path[self.time][1].real_hub

    def display_drones(self) -> None:
        for path in self.paths:
            hub = self.get_hub(path)
            x = self.x_center + self.scale * hub.x
            y = self.y_center + self.scale * hub.y
            hx = x - self.drone_icon_half
            hy = y - self.drone_icon_half
            self.screen.blit(self.drone_icon, (hx, hy))

    def display_text(self) -> None:
        text = self.font.render(f"Fly-in: {self.map.name}",
                                True, self.text_color)
        self.screen.blit(text, (int(self.padding//2), int(self.padding//2)))

    def display(self) -> None:
        clock = pygame.time.Clock()
        running = True
        max_path_len = max([len(path) for path in self.paths])
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
                        if self.time < max_path_len:
                            self.time += 1
                    if event.key == pygame.K_LEFT:
                        if self.time > -1:
                            self.time -= 1

            self.display_connections()
            self.display_hubs()
            self.display_text()
            self.display_drones()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
