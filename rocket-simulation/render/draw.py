import pygame
import math
from utils.helper import world_to_screen, calculate_angle, is_within_render_distance
from core.settings import WIDTH, HEIGHT
import numpy as np

class Draw:
    def __init__(self, window, rocket, camera, planets, height):
        self.window = window
        self.rocket = rocket
        self.camera = camera
        self.planets = planets
        self.height = height
        self.rocket_image = pygame.image.load("assets/rocket.png").convert_alpha()
        self.rocket_image = pygame.transform.scale(self.rocket_image, (int(self.rocket.size[0]), int(self.rocket.size[1])))
        self.velo = []
        for i in range(61):
            self.velo.append(0)
        self.into = int(0)

    def draw_parameters(self, steps):

        current_velocity = int(math.sqrt(self.rocket.body.velocity.x ** 2 + self.rocket.body.velocity.y ** 2))
        #
        # # Oblicz delta V
        # if self.into <= 60:
        #     self.velo[self.into] = current_velocity  # Update velocity in the list
        #     self.into += 1
        # else:
        #     ad_v = 0
        #     for i in range(60):
        #         ad_v += self.velo[i]
        #     avg = ad_v / 60
        #     self.into = 0  # Reset index after averaging
        #
        #     delta_v = current_velocity - avg
        #     print(f"ac: {delta_v / 1} m/s^2")  # Print delta V value

        # Displaying velocities and positions
        font = pygame.font.SysFont('Arial', 14)
        velocity = font.render(
            f"Velocity: {current_velocity} m/s²",
            False, (0, 0, 255)
        )
        x = font.render(
            f"x: {int(self.rocket.body.position.x - self.planets['Earth'].body.position.x)} m", True, (0, 0, 255)
        )
        y = font.render(
            f"y: {int(self.rocket.body.position.y - self.planets['Earth'].radius - self.planets['Earth'].body.position.y)} m",
            True, (0, 0, 255)
        )
        steps = font.render(
            f"Speed: {float(steps)}x",
            True, (0, 0, 255)
        )
        self.window.blit(velocity, (10, 10))
        self.window.blit(x, (10, 35))
        self.window.blit(y, (10, 60))
        self.window.blit(steps, (10, 85))

    def draw_planet(self, planet):
        screen_pos = world_to_screen(self.camera.apply(planet.body.position), self.height)
        scaled_radius = planet.radius * self.camera.zoom
        if planet.radius*self.camera.zoom > WIDTH:
            angle = calculate_angle(self.rocket, planet)
            arc_rect = (
                int(screen_pos[0] - scaled_radius),
                int(screen_pos[1] - scaled_radius),
                int(scaled_radius * 2),
                int(scaled_radius * 2)
            )
            d_angle = np.pi / (0.005 * scaled_radius)
            pygame.draw.arc(
                self.window, pygame.Color(planet.color),
                arc_rect, angle - d_angle, angle + d_angle, planet.arc_height
            )
        else:
            pygame.draw.circle(self.window, pygame.Color(planet.color),(int(screen_pos[0]),
                int(screen_pos[1])),planet.radius*self.camera.zoom)

    def draw_visible_planets(self, render_distance):
        visible_planets = filter(
            lambda planeta: is_within_render_distance(self.rocket, planeta, render_distance, self.camera.zoom),
            self.planets.values()
        )
        for planet in visible_planets:
            self.draw_planet(planet)

    def draw_rocket(self):
        scaled_size = self.camera.apply_scale(self.rocket.size)
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(self.rocket_image, (int(scaled_size[0]), int(scaled_size[1]))),
            math.degrees(self.rocket.body.angle)
        )
        rocket_pos = self.camera.apply(self.rocket.body.position)
        image_rect = rotated_image.get_rect(center=world_to_screen(rocket_pos, self.height))
        self.window.blit(rotated_image, image_rect.topleft)

    def draw_predicted_trajectory(self, trajectory):
        if len(trajectory) < 2:
            print("Trajectory too short to render.")
            return
        try:
            trajectory_points = [
                world_to_screen(self.camera.apply(pos), self.height) for pos in trajectory
            ]
            trajectory_tuples = [(point[0], point[1]) for point in trajectory_points]
            pygame.draw.lines(self.window, (255, 255, 255), False, trajectory_tuples, 1)
        except TypeError:
            print("Trajectory not found.")