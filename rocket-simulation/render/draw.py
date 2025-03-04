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
        self.flame_image = pygame.image.load("assets/flame.png").convert_alpha()
        # self.flame_image = pygame.transform.scale(self.flame_image, (int(self.rocket.size[0]), int(self.rocket.size[1])))
        self.into = int(0)

    def draw_parameters(self, steps):

        current_velocity = int(math.sqrt(self.rocket.body.velocity.x ** 2 + self.rocket.body.velocity.y ** 2))

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

        # Obrót rakiety
        angle_degrees = math.degrees(self.rocket.body.angle)
        rotated_rocket = pygame.transform.rotate(
            pygame.transform.scale(self.rocket_image, (int(scaled_size[0]), int(scaled_size[1]))),
            angle_degrees
        )

        rocket_pos = self.camera.apply(self.rocket.body.position)
        image_rect = rotated_rocket.get_rect(center=world_to_screen(rocket_pos, self.height))

        # Rysowanie rakiety
        self.window.blit(rotated_rocket, image_rect.topleft)

        # Obsługa płomienia
        if self.rocket.thrust_position > 0 and self.rocket.fuel_mass > 0:
            scale_factor = self.camera.zoom
            flame_height = int(self.flame_image.get_height() * scale_factor * (self.rocket.thrust_position / 100))

            # Skalowanie płomienia (szerokość zostaje taka sama jak rakiety)
            flame_scaled = pygame.transform.scale(self.flame_image, (int(scaled_size[0]), flame_height))
            rotated_flame = pygame.transform.rotate(flame_scaled, angle_degrees)

            # Korekcja pozycji płomienia
            flame_offset = pygame.Vector2(0, scaled_size[1] / 2 + flame_height / 2).rotate(-angle_degrees)
            flame_pos = (image_rect.centerx + flame_offset.x, image_rect.centery + flame_offset.y)

            # Rysowanie płomienia
            self.window.blit(rotated_flame, rotated_flame.get_rect(center=flame_pos).topleft)

    def draw_predicted_trajectory(self, trajectory):
        if len(trajectory) < 2:
            print("Trajectory too short to render.")
            return
        try:
            trajectory_points = [
                world_to_screen(self.camera.apply(pos), self.height) for pos in trajectory
            ]
            trajectory_tuples = [(point[0], point[1]) for point in trajectory_points]
            pygame.draw.lines(self.window, (255, 255, 255), False, trajectory_tuples, 1) # set closed to True for displacement
        except TypeError:
            print("Trajectory not found.")