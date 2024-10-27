import pymunk

class Planet:
    def __init__(self, space, name, color, position, radius_km, mass=10000):
        self.radius = radius_km * 1000
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.6
        self.shape.friction = 0.9
        self.name = name
        self.color = color

        space.add(self.body, self.shape)