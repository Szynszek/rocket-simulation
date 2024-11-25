import pymunk
import math

def apply_gravitational_force(rocket, planet):
    G = 6.674 * 10 ** -11  # Gravitational constant
    # World positions
    rocket_position = rocket.body.position
    planet_position = planet.body.position

    # Calculate the distance between the planet and the rocket
    dx = rocket_position.x - planet_position.x
    dy = rocket_position.y - planet_position.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Check to avoid division by zero
    if distance == 0:
        return

    # Calculate gravitational force
    force_magnitude = G * planet.mass * rocket.mass / distance ** 2
    force_x = force_magnitude * (dx / distance)
    force_y = force_magnitude * (dy / distance)

    # Apply gravitational force to the rocket
    force = pymunk.Vec2d(-force_x, -force_y)  # Direction towards the planet
    rocket.body.apply_force_at_world_point(force, rocket.body.position)