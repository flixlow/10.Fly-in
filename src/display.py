import pygame
from .utils import Map


class Displayer:
    def __init__(self, map: Map, background_color: str) -> None:
        self.map: Map = map
        self.background_color: str = background_color
        pygame.init()
        self.width = pygame.display.Info().current_w * (3/4)
        self.height = pygame.display.Info().current_h * (3/4)
        self._set_padding(0.10)
        self._set_origin()
        self._set_max_coordinates()
        self._set_scales()

    def _set_padding(self, padding: float) -> None:
        self.width_padding: float = self.width * padding
        self.height_padding: float = self.height * padding

    def _set_origin(self) -> None:
        self.x_center: float = self.width_padding
        self.y_center: float = self.height / 2

    def _set_max_coordinates(self) -> None:
        self.max_x: int = max(1, max([hub.x for hub in self.map.hubs]))
        self.max_y: int = max(1, max([hub.y for hub in self.map.hubs]))

    def _set_scales(self) -> None:
        usable_width = self.width - (self.width_padding * 2)
        usable_height = self.height - (self.height_padding * 2)
        self.scale: float = min(usable_width / self.max_x,
                                usable_height / self.max_y)

    def display(self) -> None:
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((self.width, self.height))

        running = True
        while running:
            screen.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            for hub in self.map.hubs:
                x = self.x_center + self.scale * hub.x
                y = self.y_center + self.scale * hub.y
                if hub.color is not None:
                    color = hub.color.value
                pygame.draw.circle(screen, color, (x, y), 20)
            for con in self.map.connections:
                start_hub = ((self.x_center + self.scale * con.start.x),
                             (self.y_center + self.scale * con.start.y))
                end_hub = ((self.x_center + self.scale * con.end.x),
                           (self.y_center + self.scale * con.end.y))
                pygame.draw.line(screen, "black", start_hub, end_hub, 3)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
