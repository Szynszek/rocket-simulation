from core.settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.offset = [0, 0]
        self.zoom = 2.0
        self.target_zoom = 2.0
        self.zoom_speed = 0.1  # zoom change speed
        self.max_zoom = 5
        self.min_zoom = 0.0000001

    def update(self, target):
        self.zoom += (self.target_zoom - self.zoom) * self.zoom_speed
        self.offset[0] = target.body.position[0] * self.zoom - WIDTH // 2
        self.offset[1] = target.body.position[1] * self.zoom - HEIGHT // 2


    def apply(self, position):
        # Scaling positions considering offset
        x = (position[0] * self.zoom - self.offset[0])
        y = (position[1] * self.zoom - self.offset[1])
        return x, y

    def apply_scale(self, size):
        return size[0] * self.zoom, size[1] * self.zoom

    def set_zoom(self, amount):
        # min_zoom < zoom < max_zoom
        self.target_zoom = max(self.min_zoom, min(self.target_zoom + amount * self.target_zoom, self.max_zoom))