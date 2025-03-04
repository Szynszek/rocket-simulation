import pygame
from pygame.locals import MOUSEWHEEL
import pymunk
from core.settings import WIDTH, HEIGHT, FPS
from render.draw import Draw
from core.camera import Camera
from entities.planet import Planet
from entities.rocket import Rocket
from utils.loader import load_json
from physics.physics import apply_gravitational_force,calculate_predicted_trajectory

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
        self.planets: dict = {
            "Earth": Planet(self.space, "Earth", (0, 0, 255), (0, 0), 6371, mass=5.972e24),

        }
        self.spawn_position_vec = self.planets[self.config["rocket"]["spawn"]].body.position
        self.spawn_position = [int(self.spawn_position_vec[0]), int(self.spawn_position_vec[1])]
        self.spawn_position[0] = int(self.spawn_position[0])
        self.spawn_position[1] += self.planets[self.config["rocket"]["spawn"]].radius + 16+1000 # 16 is rocket size

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
        """Handles user input for rocket control, zoom, and simulation speed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == MOUSEWHEEL:
                self.zoom_update(event.y / 10)

        keys = pygame.key.get_pressed()

        # Rocket thrust control (increase/decrease)
        thrust_change = (keys[pygame.K_UP] - keys[pygame.K_DOWN])  # 1 or -1
        if thrust_change:
            self.rocket.change_thrust(thrust_change)

        # Rocket rotation control (left/right)
        rotation_change = (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT])  # 1 or -1
        if rotation_change:
            self.rocket.rotate(rotation_change)

        # Camera zoom control
        if keys[pygame.K_EQUALS]:
            self.zoom_update(0.1)
        elif keys[pygame.K_MINUS]:
            self.zoom_update(-0.1)

        # Reset rocket position and velocity
        if keys[pygame.K_r]:
            self.reset_rocket()

        # Adjust simulation speed
        if keys[pygame.K_COMMA]:
            self.steps *= 0.9
        elif keys[pygame.K_PERIOD]:
            self.steps *= 1.1

    def reset_rocket(self):
        """Resets the rocket's position, velocity, and rotation."""
        self.rocket.body.position = self.spawn_position
        self.rocket.body.velocity = [0, 0]
        self.rocket.body.angle = 0
        self.steps = 1

    def zoom_update(self, value):
        """Updates the camera zoom level based on the given value."""
        self.camera.set_zoom(value)

    def update(self):
        """Updates the physics simulation, rocket thrust, camera position, and trajectory prediction."""
        self.space.step(self.steps / FPS)
        self.rocket.apply_thrust()
        self.camera.update(self.rocket)

        # Apply gravitational forces from all planets
        for planet in self.planets.values():
            apply_gravitational_force(self.rocket, planet)

        # Recalculate trajectory every 20 frames
        if self.trajectory_counter >= 20:
            self.predicted_trajectory = calculate_predicted_trajectory(self.rocket, self.planets)
            self.trajectory_counter = 0
        else:
            self.trajectory_counter += 1

    def draw(self):
        """Renders the game frame: background, planets, rocket, and trajectory."""
        self.window.blit(self.background, (0, 0))
        self.visualizations.draw_parameters(self.steps)
        self.visualizations.draw_visible_planets(self.render_distance)
        self.visualizations.draw_predicted_trajectory(self.predicted_trajectory)
        self.visualizations.draw_rocket()
        pygame.display.update()

