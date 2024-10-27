import json
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