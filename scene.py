class BaseScene:
    def __init__(self, context):
        self.context = context
        self.manager = None

    def handle_event(self, event):
        return None

    def update(self, dt):
        return None

    def draw(self, surface):
        return None


class SceneManager:
    def __init__(self, scene):
        self.scene = scene
        self.scene.manager = self

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

    def handle_event(self, event):
        self.scene.handle_event(event)

    def update(self, dt):
        self.scene.update(dt)

    def draw(self, surface):
        self.scene.draw(surface)
