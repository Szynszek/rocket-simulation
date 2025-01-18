import pygame
from pygame.locals import MOUSEWHEEL
import pymunk
from core.settings import WIDTH, HEIGHT, FPS
from render.draw import Draw
from core.camera import Camera
from entities.planet import Planet
from entities.rocket import Rocket
from utils.loader import load_json
from physics.forces import apply_gravitational_force
from utils.helper import calculate_predicted_trajectory

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rocket Physics Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        self.space = pymunk.Space()
        self.config = load_json('config/config.json')
        self.background = pygame.image.load("assets/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.planets = {
            "Earth": Planet(self.space, "Earth", (0, 0, 255), (400, 0), 6371, mass=5.972e24),
            "1": Planet(self.space, "1", (0, 255, 0), (-400, 6372300), 0.5, mass=1.7e17),
            "2": Planet(self.space, "2", (255, 0, 0), (1260, 6372300), 0.5, mass=1.7e17)
        }
        self.spawn_position_vec = self.planets[self.config["rocket"]["spawn"]].body.position
        self.spawn_position = [int(self.spawn_position_vec[0]), int(self.spawn_position_vec[1])]
        self.spawn_position[0] = int(35 + self.spawn_position[0])
        self.spawn_position[1] += self.planets[self.config["rocket"]["spawn"]].radius + 35

        self.rocket = Rocket(self.space, self.spawn_position)
        self.camera = Camera()
        self.visualizations = Draw(self.window, self.rocket, self.camera, self.planets, HEIGHT)
        self.steps = 1
        self.predicted_trajectory = []
        self.trajectory_counter = 10
        self.render_distance = ((WIDTH**2+HEIGHT**2)**0.5)/2

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == MOUSEWHEEL:
                self.zoom_update(event.y / 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rocket.apply_thrust(3000000)
        if keys[pygame.K_LEFT]:
            self.rocket.rotate(1)
        if keys[pygame.K_RIGHT]:
            self.rocket.rotate(-1)
        if keys[pygame.K_EQUALS]:
            self.zoom_update(0.1)
        if keys[pygame.K_MINUS]:
            self.zoom_update(-0.1)
        if keys[pygame.K_r]:
            self.rocket.body.position = self.spawn_position
            self.rocket.body.velocity = [0, 0]
            self.rocket.body.angle = 0
        if keys[pygame.K_COMMA]:
            self.steps *= 0.9
        if keys[pygame.K_PERIOD]:
            self.steps *= 1.1

    def zoom_update(self, value):
        self.camera.set_zoom(value)

    def update(self):
        self.space.step(1 * self.steps / FPS)
        self.camera.update(self.rocket)
        for planet in self.planets.values():
            apply_gravitational_force(self.rocket, planet)

        # Calculate trajectory every 10 frames
        self.trajectory_counter += 1
        if self.trajectory_counter >= 10:

            self.predicted_trajectory = calculate_predicted_trajectory(self.rocket, self.planets)
            self.trajectory_counter = 0

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.visualizations.draw_parameters(self.steps)
        self.visualizations.draw_visible_planets(render_distance=self.render_distance)
        self.visualizations.draw_predicted_trajectory(self.predicted_trajectory)
        self.visualizations.draw_rocket()
        pygame.display.update()
