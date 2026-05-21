import pygame  # type: ignore
from .utils import Map
import json


class Displayer:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.set_screen()
        self.set_padding(0.10)
        self.set_origin()
        self.set_max_coordinates()
        self.set_scales()
        self.set_colors()

    def set_screen(self) -> None:
        pygame.init()

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
        self.max_x: int = max(1, max([hub.x for hub in self.map.hubs]))
        self.max_y: int = max(1, max([hub.y for hub in self.map.hubs]))

    def set_scales(self) -> None:
        usable_width = self.width - (self.padding * 2)
        usable_height = self.height - (self.padding * 2)
        self.scale: float = min(usable_width / self.max_x,
                                usable_height / self.max_y)

    def set_colors(self) -> None:
        with open("src/assets/themes.json", "r") as f:
            data = json.load(f)
        self.themes = data
        self.current_theme = 0
        self.font = pygame.font.Font("src/assets/Tanker-Regular.otf", 60)

        self.back_color: tuple[int, int, int] = self.themes[0]["back"]
        self.line_color: tuple[int, int, int] = self.themes[0]["line"]
        self.text_color: tuple[int, int, int] = self.themes[0]["text"]

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
                             start_hub, end_hub, 5)

    def display_hubs(self) -> None:
        for hub in self.map.hubs:
            x = self.x_center + self.scale * hub.x
            y = self.y_center + self.scale * hub.y
            if hub.color is not None:
                color = hub.color.value
            pygame.draw.circle(self.screen, color, (x, y), 20)
            pygame.draw.circle(self.screen, self.line_color, (x, y), 15)

    def display_drones(self) -> None:
        ...

    def display_text(self) -> None:
        text = self.font.render(f"Fly-in: {self.map.name}",
                                True, self.text_color)
        self.screen.blit(text, (self.padding, self.padding))

    def display(self) -> None:
        clock = pygame.time.Clock()
        running = True
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

            self.display_connections()
            self.display_hubs()
            self.display_drones()
            self.display_text()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
