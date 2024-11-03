import pymunk

class Planet:
    def __init__(self, space, name, color, position, radius_km, scale, mass):
        self.radius = radius_km * 1000
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.6
        self.shape.friction = 0.9
        self.name = name
        self.color = color
        self.scale = scale
        self.arc_height = 0
        self.set_arc_height((800,600))
        self.mass = mass

        space.add(self.body, self.shape)

    def set_arc_height(self, screen_size):
        distance_to_corner = (screen_size[0]**2+screen_size[1]**2)/2
        if self.radius*self.scale < distance_to_corner:
            self.arc_height = int(self.radius)
        elif self.radius*self.scale > 6400000:
            self.arc_height = int(screen_size[1]/2)
        else:
            self.arc_height = int(-0.0000314*self.radius*self.scale+501)
