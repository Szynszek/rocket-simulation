import pymunk
from core.settings import WIDTH, HEIGHT
class Planet:
    def __init__(self, space, name, color, position, radius_km, mass):
        # self.base_radius = radius_km * 1000 # convert to meters
        self.radius = radius_km * 1000
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.6
        self.shape.friction = 0.9
        self.name = name
        self.color = color
        self.mass = mass
        self.arc_height = self.calculate_arc_height()

        space.add(self.body, self.shape)

    def calculate_arc_height(self):
        distance_to_corner = ((WIDTH**2+HEIGHT**2)**(1/2))/2
        if self.radius < distance_to_corner:
            return int(self.radius)
        elif self.radius > 6000000:
            return int(distance_to_corner)
        else:
            return int(-0.0000314*self.radius+501)