import numpy as np
import pygame
import math
from utils import world_to_screen, calculate_angle, apply_gravitational_force


BLUE = (0, 0, 255)
WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)


class Draw:
    def __init__(self, window, rocket, camera, planets):
        self.window = window
        self.rocket = rocket
        self.camera = camera
        self.planets = planets
        self.rocket_image = pygame.image.load("rocket-simulation/assets/rocket.png").convert_alpha()
        self.rocket_image = pygame.transform.scale(self.rocket_image, (int(self.rocket.size[0]), int(self.rocket.size[1])))

    def draw_parameters(self):
        # Drawing rocket parameters on screen
        font = pygame.font.SysFont('Arial', 14)
        velocity = font.render(f"Velocity: {int(math.sqrt(self.rocket.body.velocity[0]**2 + self.rocket.body.velocity[1]**2))} m/s²", False, BLUE)
        x = font.render(f"x: {int(self.rocket.body.position[0] - self.planets["Earth"].body.position[0])} m", True, BLUE)
        y = font.render(f"y: {int(self.rocket.body.position[1] - self.planets["Earth"].radius - self.planets["Earth"].body.position[1])} m", True, BLUE)
        self.window.blit(velocity, (10, 10))
        self.window.blit(x, (10, 35))
        self.window.blit(y, (10, 60))

    def draw_planets(self, planets, scale):
        for planet in planets.values():
            # Rocket position relative to the planet
            dx = self.rocket.body.position[0] - planet.body.position[0]
            dy = self.rocket.body.position[1] - planet.body.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2) - planet.radius

            if distance < 1000:
                screen_pos = world_to_screen(self.camera.apply(planet.body.position), HEIGHT)
                angle = calculate_angle(self.rocket, planet)
                apply_gravitational_force(self.rocket, screen_pos, planet.mass, world_to_screen(self.camera.apply(self.rocket.body.position), HEIGHT), scale)
                # ^^ will be moved to right class

                # Parameter for drawing arc
                arc_rect = (
                    int(screen_pos[0] - planet.radius),
                    int(screen_pos[1] - planet.radius),
                    int(planet.radius * 2),
                    int(planet.radius * 2)
                )
                d_angle = np.pi / (0.006 * planet.radius)
                arc_width = planet.arc_height
                pygame.draw.arc(
                    self.window, pygame.Color(planet.color),
                    arc_rect, angle - d_angle, angle + d_angle, arc_width
                )

    def draw_rocket(self):
        # Rotate the image based on the rocket's angle
        rotated_image = pygame.transform.rotate(self.rocket_image, math.degrees(self.rocket.body.angle))
        rocket_pos = self.camera.apply(self.rocket.body.position)

        # Adjust position to ensure image center aligns with rocket position
        image_rect = rotated_image.get_rect(center=world_to_screen(rocket_pos, HEIGHT))

        # Draw the rotated image
        self.window.blit(rotated_image, image_rect.topleft)

class Camera:
    def __init__(self):
        self.offset = [0, 0]
    def update(self, target):
        # Setting the camera to track the rocket
        self.offset[0] = target.body.position[0] - WIDTH // 2
        self.offset[1] = target.body.position[1] - HEIGHT // 2
    def apply(self, position):
        # Shifting the object position by the camera offset
        return position[0] - self.offset[0], position[1] - self.offset[1]
    

