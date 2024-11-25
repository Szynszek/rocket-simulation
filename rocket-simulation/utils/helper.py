import math
import pymunk
from scipy.integrate import solve_ivp

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
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance <= (render_distance/zoom) + planet.radius

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
            distance = math.sqrt(dx**2 + dy**2)

            if distance < MIN_DISTANCE:
                continue  # Ignore too small distances

            # Limit the gravitational force
            force_magnitude = min(G * planet.mass * rocket.mass / distance**2, MAX_FORCE)
            force_x = -force_magnitude * (dx / distance)
            force_y = -force_magnitude * (dy / distance)
            total_force_x += force_x
            total_force_y += force_y

        # Acceleration
        ax = total_force_x / rocket.mass
        ay = total_force_y / rocket.mass
        return [vx, vy, ax, ay]

    # Termination condition: the rocket reaches the planet's surface
    def hit_surface(t, state):
        x, y, vx, vy = state
        for planet in planets.values():
            dx = x - planet.body.position.x
            dy = y - planet.body.position.y
            distance = math.sqrt(dx**2 + dy**2)
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
    velocity = math.sqrt(initial_state[2]**2 + initial_state[3]**2)
    step_size = 0.00001 * velocity**2 + 0.1
    solution = solve_ivp(
        dynamics,
        (0, 100000),
        initial_state,
        method='RK45',
        events=hit_surface,  # Termination condition
        max_step=step_size,
        rtol=1e-6,
        atol=1e-9
    )

    # Extracting position (x, y) from the solution
    trajectory = [pymunk.Vec2d(x, y) for x, y in zip(solution.y[0], solution.y[1])]


    return trajectory