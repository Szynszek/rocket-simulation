import numpy as np
import pygame
import math
from utils import world_to_screen, calculate_angle


BLUE = (0, 0, 255)
WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)


class Draw:
    def __init__(self, window, rocket, camera, planets):
        self.window = window
        self.rocket = rocket
        self.camera = camera
        self.planets = planets

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

                # Parameter for drawing arc
                arc_rect = (
                    int(screen_pos[0] - planet.radius),
                    int(screen_pos[1] - planet.radius),
                    int(planet.radius * 2),
                    int(planet.radius * 2)
                )
                d_angle = np.pi / (0.006 * planet.radius)
                arc_width = int(-0.000000314*(planet.radius*scale)+500)
                if arc_width <=0: arc_width = 200
                pygame.draw.arc(
                    self.window, pygame.Color(planet.color),
                    arc_rect, angle - d_angle, angle + d_angle, arc_width
                )

    def draw_rocket(self):
        vertices = [self.camera.apply(v.rotated(self.rocket.body.angle) + self.rocket.body.position) for v in self.rocket.shape.get_vertices()]
        pygame.draw.polygon(self.window, RED, [world_to_screen(v, HEIGHT) for v in vertices])

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
    

