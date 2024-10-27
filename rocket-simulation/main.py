import pygame
import pymunk

from planets import Planet
from rocket import Rocket
from visualizations import Draw, Camera
from utils import load_json


# Pygame Initialization
pygame.init()

# Game window parameters
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Physics Simulation")

# Color settings
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
BLUE = (0, 0, 255)
GROUND_COLOR = (139, 69, 19)

# Scale 1 = 1 meter is 1 px
# Scale 2 = 2 meters is 1 px
SCALE = 30
FPS = 144
space = pymunk.Space()

config = load_json('config.json')
rocket_config = config["rocket"]

space.gravity = (0, -9.81 * SCALE)


planets = {"Earth": Planet(space,"Earth", BLUE, (400 * SCALE, 6371 * SCALE), 6371*SCALE),
           "Mars": Planet(space,"Mars", RED, (400 * SCALE, 6378371 * SCALE), 0.1*SCALE)}

spawn_position = planets[rocket_config["spawn"]].body.position

# Rocket launch position on the planet's surface
rocket_spawn_position = (spawn_position[0], spawn_position[1] + planets[rocket_config["spawn"]].radius + (7 * SCALE) / 2)


rocket = Rocket(space, rocket_spawn_position , scale=SCALE)
camera = Camera()
visualizations = Draw(window, rocket, camera, planets)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # Rocket Controls: Forward Thrust and Spin
    if keys[pygame.K_UP]:
        rocket.apply_thrust(100)
    if keys[pygame.K_LEFT]:
        rocket.rotate(1)
    if keys[pygame.K_RIGHT]:
        rocket.rotate(-1)

    space.step(1 / FPS)
    camera.update(rocket)

    window.fill(BLACK)

    visualizations.draw_parameters()
    visualizations.draw_planets(planets, SCALE)
    visualizations.draw_rocket()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

