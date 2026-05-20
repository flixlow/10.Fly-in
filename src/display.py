import pygame
from .utils import Map


class Displayer:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        pygame.init()
        self.width = pygame.display.Info().current_w * (3/4)
        self.height = pygame.display.Info().current_h * (3/4)
        self._set_padding(0.10)
        self._set_origin()
        self._set_max_coordinates()
        self._set_scales()
        self.font = pygame.font.Font("src/assets/Tanker-Regular.otf", 60)
        self.themes = [
                {
                    "back": (236, 239, 244),
                    "line": (94, 129, 172),
                    "text": (46, 52, 64),
                },
                {
                    "back": (20, 20, 30),
                    "line": (0, 255, 180),
                    "text": (255, 0, 140),
                },
                {
                    "back": (240, 245, 235),
                    "line": (87, 117, 77),
                    "text": (124, 92, 70),
                },
                {
                    "back": (224, 247, 250),
                    "line": (0, 96, 100),
                    "text": (38, 70, 83),
                },
                {
                    "back": (255, 236, 214),
                    "line": (231, 111, 81),
                    "text": (106, 76, 147),
                },
                {
                    "back": (24, 24, 27),
                    "line": (113, 113, 122),
                    "text": (244, 244, 245),
                },
                {
                    "back": (155, 188, 15),
                    "line": (48, 98, 48),
                    "text": (15, 56, 15),
                },
                {
                    "back": (245, 240, 255),
                    "line": (186, 104, 200),
                    "text": (94, 53, 177),
                },
                {
                    "back": (34, 17, 17),
                    "line": (255, 87, 34),
                    "text": (255, 193, 7),
                },
                {
                    "back": (0, 10, 0),
                    "line": (0, 255, 70),
                    "text": (180, 255, 180),
                }
            ]

        self.current_theme = 0

        self.background_color: tuple[int, int, int] = self.themes[0]["back"]
        self.line_color: tuple[int, int, int] = self.themes[0]["line"]
        self.text_color: tuple[int, int, int] = self.themes[0]["text"]

    def change_theme(self) -> None:
        self.current_theme += 1

        if self.current_theme >= len(self.themes):
            self.current_theme = 0

        theme = self.themes[self.current_theme]

        self.background_color = theme["back"]
        self.line_color = theme["line"]
        self.text_color = theme["text"]

    def _set_padding(self, padding: float) -> None:
        width_padding: float = self.width * padding
        height_padding: float = self.height * padding
        self.padding = max(width_padding, height_padding)

    def _set_origin(self) -> None:
        self.x_center: float = self.padding
        self.y_center: float = self.height / 2

    def _set_max_coordinates(self) -> None:
        self.max_x: int = max(1, max([hub.x for hub in self.map.hubs]))
        self.max_y: int = max(1, max([hub.y for hub in self.map.hubs]))

    def _set_scales(self) -> None:
        usable_width = self.width - (self.padding * 2)
        usable_height = self.height - (self.padding * 2)
        self.scale: float = min(usable_width / self.max_x,
                                usable_height / self.max_y)

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

    def display_text(self) -> None:
        text = self.font.render(f"Fly-in: {self.map.name}",
                                True, self.text_color)
        self.screen.blit(text, (self.padding, self.padding))

    def display(self) -> None:
        clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))

        running = True
        while running:
            self.screen.fill(self.background_color)
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
            self.display_text()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
