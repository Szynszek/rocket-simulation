import pymunk

class Rocket:
    def __init__(self, space, position, size=(16, 32), mass=10000, start_angle=0):
        self.size = (size[0], size[1])
        self.netto_mass = mass
        self.fuel_mass = 200000 # kilograms
        self.fuel_stream = 10/60 # How many kilograms of fuel used per simulation tick for 1 point of thrust_position
        self.mass = self.netto_mass+self.fuel_mass
        moment = pymunk.moment_for_box(self.mass, (8,32))
        self.body = pymunk.Body(self.mass, moment)
        self.body.position = position
        self.body.angle = start_angle

        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 0.4
        self.shape.friction = 0.5
        self.thrust_position = 0
        self.thrust_power = 38000 # How many Newtons per 1 point of thrust_position
        self.thrust = 0

        space.add(self.body, self.shape)

    def change_thrust(self, change):
        self.thrust_position = min(max(self.thrust_position + change, 0), 100)
        self.thrust = self.thrust_position*self.thrust_power

    def burn_fuel(self):
        self.fuel_mass -= self.fuel_stream*self.thrust_position
        self.body.mass = self.fuel_mass + self.netto_mass

    def get_thrust(self):
        if self.fuel_mass <= 0 or self.thrust_position <= 0.5:
            return pymunk.Vec2d(0, 0)

        force = pymunk.Vec2d(0, self.thrust).rotated(self.body.angle)
        return force

    def rotate(self, angle_change):
        self.body.angular_velocity += angle_change * 0.03