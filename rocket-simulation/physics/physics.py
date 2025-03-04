import math

import numpy as np
import pymunk
from scipy.integrate import solve_ivp

from utils import helper


def apply_gravitational_force(rocket, planet):
    G = 6.6743 * 10 ** -11  # Gravitational constant
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
    force_magnitude = G * planet.mass * rocket.body.mass / (distance ** 2)
    force_x = force_magnitude * (dx / distance)
    force_y = force_magnitude * (dy / distance)

    # Apply gravitational force to the rocket
    force = pymunk.Vec2d(-force_x, -force_y)  # Direction towards the planet
    rocket.body.apply_force_at_world_point(force, rocket.body.position)
    acceleration = force_magnitude / rocket.body.mass
    stop_rotation(rocket)
    # print(calculate_orbital_energy(rocket))

def calculate_predicted_trajectory(rocket, planets):
    """
    Predicts the rocket's trajectory considering variable gravity
    and calculates the time to fall to the surface of the nearest planet.
    """

    def dynamics(t, state):
        """
        Function describing the rocket's dynamics.
        """
        x, y, vx, vy = state
        total_force_x = 0
        total_force_y = 0
        G = 6.6743 * 10 ** -11  # Gravitational constant
        MIN_DISTANCE = 1  # Minimum distance
        MAX_FORCE = 1e10  # Maximum gravitational force

        for planet in planets.values():
            dx = x - planet.body.position.x
            dy = y - planet.body.position.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < MIN_DISTANCE:
                continue  # Ignore too small distances

            # Limit the gravitational force
            force_magnitude = min(G * planet.mass * rocket.body.mass / distance ** 2, MAX_FORCE)
            force_x = -force_magnitude * (dx / distance)
            force_y = -force_magnitude * (dy / distance)
            total_force_x += force_x
            total_force_y += force_y

        # Acceleration
        ax = total_force_x / rocket.body.mass
        ay = total_force_y / rocket.body.mass
        return [vx, vy, ax, ay]

    # Termination condition: the rocket reaches the planet's surface
    def hit_surface(t, state):
        x, y, vx, vy = state
        for planet in planets.values():
            dx = x - planet.body.position.x
            dy = y - planet.body.position.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= planet.radius:
                return 0  # The rocket reached the surface
        return 1  # Continue simulation

    hit_surface.terminal = True
    hit_surface.direction = -1  # The function ends when approaching the surface

    # Initial state of the rocket
    initial_state = [
        rocket.body.position.x,
        rocket.body.position.y,
        rocket.body.velocity.x,
        rocket.body.velocity.y,
    ]
    closest: list = [999999999999,1,1]
    for planet in planets.values():
        dx = rocket.body.position.x - planet.body.position.x
        dy = rocket.body.position.y - planet.body.position.y
        distance = math.sqrt(dx ** 2 + dy ** 2)-planet.radius
        if distance < closest[0]:
            closest[0] = distance
            closest[1] = planet
    velocity = math.sqrt(initial_state[2] ** 2 + initial_state[3] ** 2)
    G=6.6743 * 10 ** -11
    print(math.sqrt(G*closest[1].mass/(closest[0]+closest[1].radius))-100)

    ang = helper.calculate_angle(rocket, closest[1])
    v_tangential = math.sqrt((rocket.body.velocity.x*math.cos(ang-math.pi/2))**2+(rocket.body.velocity.y*math.sin(ang-math.pi/2))**2)

    # print(math.sqrt(1+2*calculate_orbital_energy(rocket)*))
    if velocity <= math.sqrt(G*closest[1].mass/(closest[0]+closest[1].radius))-100:
        step_size = 0.000001*(0.1*closest[0]**2+velocity**2)+0.1
    else:
        step_size = 0.0001 * velocity ** 3 + 0.1
    solution = solve_ivp(
        dynamics,
        (0, 1e5),
        initial_state,
        method='RK45',
        events=hit_surface,
        max_step=step_size,
        rtol=1e-6,
        atol=1e-9,
        dense_output=True  # Dodaj to
    )

    trajectory = []
    if solution.t_events[0].size > 0:
        t_impact = solution.t_events[0][0]
        t_eval = np.linspace(0, t_impact, 300)
        y_eval = solution.sol(t_eval)
        trajectory = [pymunk.Vec2d(x, y) for x, y in zip(y_eval[0], y_eval[1])]
    else:
        trajectory = [pymunk.Vec2d(x, y) for x, y in zip(solution.y[0], solution.y[1])]
    print(len(trajectory))
    return trajectory

def stop_rotation(rocket): # temporary function
    if 0.02 > rocket.body.angular_velocity > -0.02:
        rocket.body.angular_velocity = 0
        return
    if 0.5 < rocket.body.angular_velocity < -0.5:
        rocket.body.angular_velocity *= 0.098
        return
    rocket.body.angular_velocity *= 0.994

def calculate_orbital_energy(rocket):
    G = 6.6743 * 10 ** -11
    px = rocket.body.position.x
    py = rocket.body.position.y
    r = math.sqrt(px ** 2 + py ** 2)
    vx = rocket.body.velocity.x
    vy = rocket.body.velocity.y
    v = math.sqrt(vx**2 + vy**2)
    return v**2/2 - (G*5.972e24/r)

