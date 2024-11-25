import pymunk

class Rocket:
    def __init__(self, space, position, size=(2*10, 7*10), mass=10000, angle=0):
        self.size = (size[0], size[1])
        self.mass = mass
        moment = pymunk.moment_for_box(mass, self.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position
        self.body.angle = angle
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def apply_thrust(self, thrust):
        force = pymunk.Vec2d(0, thrust).rotated(self.body.angle)
        self.body.apply_force_at_world_point(force, self.body.position)

    def rotate(self, angle_change):
        self.body.angular_velocity += angle_change * 0.01