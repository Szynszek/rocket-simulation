import json
import math

import numpy as np

def load_json(filename):
    with open("rocket-simulation/" + filename, 'r') as f:
        return json.load(f)

def world_to_screen(position, height):
    # Inverting the Y axis, since pymunk counts Y "up" and Pygame "down"
    return int(position[0]), int(height - position[1])

def calculate_angle(poly, circle):
    # Positions of the centers of the bodies
    start = np.array(circle.body.position)
    end_a = np.array(poly.body.position)
    # The angle between the rocket-planet vector and the vertical
    dx, dy = end_a - start
    theta_radians = np.arctan2(dy, dx)
    return theta_radians

def apply_gravitational_force(rocket, planet_c, planet_m, rocket_c, scale):

    G = 6.674 * 10 ** -11
    M = planet_m

    # Współrzędne punktów
    x_p, y_p = rocket_c
    x_s, y_s = planet_c

    # Oblicz odległość r
    r = math.sqrt((x_p - x_s) ** 2 + (y_p - y_s) ** 2)

    # Składowe przyspieszenia grawitacyjnego
    a_x = G * M * (x_s - x_p) / r ** 3
    a_y = G * M * (y_s - y_p) / r ** 3

    # Przekształcamy przyspieszenie na siłę
    force_x = rocket.mass * a_x * scale
    force_y = rocket.mass * -a_y * scale
    print(force_x, force_y)

    # Nakładamy siłę na ciało poly w globalnym układzie współrzędnych
    # rocket.body.apply_force_at_world_point((round(force_x), round(force_y)), (0,0))
    rocket.body.apply_force_at_world_point((force_x, force_y), rocket.body.position)