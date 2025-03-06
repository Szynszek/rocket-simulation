import pygame
import math
from utils.helper import world_to_screen, calculate_angle, is_within_render_distance
from core.settings import WIDTH
from pygame.sprite import Group
from render.sprites import rocket_sprite, flame_sprite

class Draw:
    def __init__(self, window, rocket, camera, planets, height):
        self.window = window
        self.rocket = rocket
        self.camera = camera
        self.planets = planets
        self.height = height
        self.font = pygame.font.SysFont('Arial', 14)
        self.static_text = {
            'velocity': self.font.render("Velocity: ", True, (0, 0, 255)),
            'x': self.font.render("X: ", True, (0, 0, 255)),
            'y': self.font.render("Y: ", True, (0, 0, 255)),
            'speed': self.font.render("Sim. speed: ", True, (0, 0, 255)),
            'fuel': self.font.render("Fuel: ", True, (0, 0, 255)),
        }
        self.text_distance = 25
        self.last_zoom = None
        self.last_angle = None

        self.rocket_group = Group()
        self.flame_group = Group()

        self.rocket_sprite = rocket_sprite.RocketSprite(rocket, camera)
        self.flame_sprite = flame_sprite.FlameSprite(rocket, camera)

        self.rocket_group.add(self.rocket_sprite)
        self.flame_group.add(self.flame_sprite)


    def draw_parameters(self, steps):

        velocity_val = self.font.render(
            f"{int(math.hypot(self.rocket.body.velocity.x, self.rocket.body.velocity.y))} m/s", True, (0, 0, 255))
        x_val = self.font.render(f"{int(self.rocket.body.position.x - self.planets['Earth'].body.position.x)} m", True, (0, 0, 255))
        y_val = self.font.render(f"{int(self.rocket.body.position.y - self.planets['Earth'].radius - self.planets['Earth'].body.position.y)} m", True, (0, 0, 255))
        steps_val = self.font.render(f"{float(steps)}x", True, (0, 0, 255))
        fuel_val = self.font.render(f"{int(self.rocket.fuel_mass)} kg", True, (0, 0, 255))

        for i, val in enumerate(self.static_text.values(),1):
            self.window.blit(val, (10, 25*i))

        self.window.blit(velocity_val, (100, 25))
        self.window.blit(x_val, (100, 50))
        self.window.blit(y_val, (100, 75))
        self.window.blit(steps_val, (100, 100))
        self.window.blit(fuel_val, (100, 125))

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
            d_angle = math.pi / (0.005 * scaled_radius)
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
        # Automatic update by groups
        self.rocket_group.update()
        self.flame_group.update()

        self.rocket_group.draw(self.window)
        if self.rocket.thrust_position > 0 and self.rocket.fuel_mass > 0:
            self.flame_group.add(self.flame_sprite)
            self.flame_group.draw(self.window)
        else:
            self.flame_group.remove(self.flame_sprite)

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