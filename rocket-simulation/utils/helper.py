import math

def world_to_screen(position, height):
    """
    Converts a position from world coordinates to screen coordinates.
    The Y-axis is reversed because Pygame has the Y-axis growing downward.
    """
    return int(position[0]), int(height - position[1])

def calculate_angle(rocket, planet):
    """
    Calculates the angle between the rocket and the planet in radians.
    """
    dx = rocket.body.position.x - planet.body.position.x
    dy = rocket.body.position.y - planet.body.position.y
    theta_radians = math.atan2(dy, dx)
    return theta_radians

def is_within_render_distance(rocket, planet, render_distance, zoom=1):
    """
    Checks if the planet is within the render range relative to the rocket.
    """
    dx = rocket.body.position.x - planet.body.position.x
    dy = rocket.body.position.y - planet.body.position.y
    max_distance = (render_distance / zoom) + planet.radius
    dx_sq = dx ** 2
    dy_sq = dy ** 2
    return (dx_sq + dy_sq) <= max_distance ** 2