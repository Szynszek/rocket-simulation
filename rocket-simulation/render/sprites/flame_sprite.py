import pygame
import math
from core.camera import Camera
from entities.rocket import Rocket


class FlameSprite(pygame.sprite.Sprite):
    def __init__(self, rocket: Rocket, camera: Camera):
        super().__init__()
        self.rocket = rocket
        self.camera = camera
        self.supersample_factor = 4

        # Loading and preparing the texture
        self.original_image = pygame.image.load("assets/flame.png").convert_alpha()
        self.base_height = self.original_image.get_height() // self.supersample_factor
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.offset_vector = pygame.Vector2()

        self._current_zoom = 1.0
        self._current_angle = 0.0
        self._current_thrust = 0
        self._update_transform()

    def _should_redraw(self) -> bool:
        return (
                self.rocket.thrust_position != self._current_thrust or
                not math.isclose(self.camera.zoom, self._current_zoom, rel_tol=1e-3) or
                not math.isclose(math.degrees(self.rocket.body.angle), self._current_angle, rel_tol=1e-3)
        )

    def _update_transform(self):
        # Calculating the height of the flame in the game world
        base_flame_height = self.base_height * (self.rocket.thrust_position / 100)

        # Scaling to the game world with camera included
        target_height = int(base_flame_height * self.camera.zoom)
        target_width = int(self.rocket.size[0] * self.camera.zoom)

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

        # Calculate offset
        rocket_height = self.rocket.size[1] * self.camera.zoom
        self.offset_vector = pygame.Vector2(0, (rocket_height + target_height) / 2).rotate(
            -math.degrees(self.rocket.body.angle)
        )

        self.rect = self.image.get_rect()
        self._current_zoom = self.camera.zoom
        self._current_angle = math.degrees(self.rocket.body.angle)
        self._current_thrust = self.rocket.thrust_position

    def update(self):
        if not self.rocket.fuel_mass > 0 or self.rocket.thrust_position <= 0.5:
            self.kill()
            return

        if self._should_redraw():
            self._update_transform()

        rocket_center = self.camera.apply(self.rocket.body.position)
        self.rect.center = (
            rocket_center[0] + self.offset_vector.x,
            rocket_center[1] + self.offset_vector.y
        )