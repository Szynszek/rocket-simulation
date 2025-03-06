import pymunk
import core.settings as settings
class Planet:
    def __init__(self, space, name, color, position, radius_km, mass):
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
        if self.radius < settings.DIAGONAL:
            return int(self.radius)
        elif self.radius > 6000000:
            return int(settings.DIAGONAL)
        else:
            return int(-0.0000314*self.radius+501)