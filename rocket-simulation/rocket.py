import pymunk

class Rocket:
    def __init__(self, space, position, size=(2, 7), mass=1, angle=0, scale=10):
        # scaling size
        self.SCALE = scale
        self.size = (size[0] * self.SCALE, size[1] * self.SCALE)
        self.mass = mass

        # Creating body of the rocket
        moment = pymunk.moment_for_box(mass, self.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position
        self.body.angle = angle

        # Rocket shape is rectangle
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        # Adding rocket to space
        space.add(self.body, self.shape)

    def apply_thrust(self, thrust):
        force = pymunk.Vec2d(0, thrust*self.SCALE)

        # Rotation of the force vector depending on the angle of the rocket (self.body.angle)
        rotated_force = force.rotated(self.body.angle)

        # Applying force to the rocket position
        self.body.apply_force_at_world_point(rotated_force, self.body.position)



    def rotate(self, angle_change):
        self.body.angular_velocity += angle_change*0.2