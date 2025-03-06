import pygame
import math
from core.camera import Camera
from entities.rocket import Rocket


class RocketSprite(pygame.sprite.Sprite):
    def __init__(self, rocket: Rocket, camera: Camera):
        super().__init__()
        self._last_transform = None
        self.rocket = rocket
        self.camera = camera
        self.supersample_factor = 4

        # Loading and preparing the texture
        self.original_image = pygame.image.load("assets/rocket.png").convert_alpha()
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)

        self._current_zoom = 1.0
        self._current_angle = 0.0
        self._update_transform()

    def _should_redraw(self) -> bool:
        return (
                not math.isclose(self.camera.zoom, self._current_zoom, rel_tol=1e-3) or
                not math.isclose(math.degrees(self.rocket.body.angle), self._current_angle, rel_tol=1e-3)
        )

    def _update_transform(self):
        if self._last_transform == (self.camera.zoom, self.rocket.body.angle):
            return
        # Target size in the game world
        target_width = int(self.rocket.size[0] * self.camera.zoom)
        target_height = int(self.rocket.size[1] * self.camera.zoom)

        # Supersampling transformations
        scaled = pygame.transform.smoothscale(
            self.original_image,
            (target_width * self.supersample_factor, target_height * self.supersample_factor)
        )
        self.image = pygame.transform.rotozoom(
            scaled,
            math.degrees(self.rocket.body.angle),
            1 / self.supersample_factor  # Supersampling compensation
        )

        self.rect = self.image.get_rect()
        self._current_zoom = self.camera.zoom
        self._current_angle = math.degrees(self.rocket.body.angle)
        self._last_transform = (self.camera.zoom, self.rocket.body.angle)

    def update(self):
        if self._should_redraw():
            self._update_transform()

        screen_pos = self.camera.apply(self.rocket.body.position)
        self.rect.center = screen_pos