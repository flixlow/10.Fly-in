import pygame
from .utils import Map


class Displayer:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        pygame.init()
        self.width = pygame.display.Info().current_w * (3/4)
        self.height = pygame.display.Info().current_h * (3/4)
        self.width_padding = self.width * 0.05
        self.height_padding = self.height * 0.05
        self.x_center = self.width // 2
        self.y_center = self.height // 2
        self.max_coords = max([max(hub.x, hub.y) for hub in map.hubs]) * 2
        self.x_scale = (self.width - (self.width_padding * 2)) // self.max_coords
        self.y_scale = (self.height - (self.height_padding * 2)) // self.max_coords

    def display(self) -> None:
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((self.width, self.height))

        running = True
        while running:
            screen.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            for hub in self.map.hubs:
                x = self.x_center + self.x_scale * hub.x
                y = self.y_center + self.y_scale * hub.y
                if hub.color is not None:
                    color = hub.color.value
                pygame.draw.circle(screen, color, (x, y), 20)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
