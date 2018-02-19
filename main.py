from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from random import randint
import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', 0)
from kivy.core.window import Window


class Game(FloatLayout):
    player = ObjectProperty(None)
    ground = ObjectProperty(None)
    ceiling = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.clock = Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.walls = []
        self.time = 120
        self.spawnWall()

    def update(self, dt):
        self.player.move(self.player.gravity)
        self.moveWalls()
        for i in self.walls:
            if self.player.collide_widget(i):
                self.clock.cancel()
        if self.time > 30:
            self.time -= 0.1
        if randint(0, int(self.time)) == 1:
            self.spawnWall()

    def reset(self):
        self.clock.cancel()
        if self.walls:
            self.clear_widgets(children=self.walls)
            self.walls = []
        self.time = 120
        self.player.reset()
        self.clock()

    def spawnWall(self):
        d = Wall()
        self.walls.append(d)
        self.add_widget(d)

    def moveWalls(self):
        for i in self.walls:
            i.move()
            if i.x < (0 - i.width):
                self.walls.remove(i)


class Player(Widget):
    vector = Vector(0, 0)
    jumps = NumericProperty(5)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.pos = (50, (Window.height * 0.162))
        self.jumps = 5
        self.left = Window.width / 2
        self.up = Window.height * 0.13
        self.gravity = Vector(0, -0.0002777777777778 * Window.height)
        self.ground = (Window.height * 0.13)
        self.ceiling = (Window.height - (Window.height * (0.13 + .064)))
        self.vl = (Window.height * 0.0676) / 5

    def on_touch_down(self, touch):
        if touch.y < self.up:
            if touch.x < self.left and self.jumps > 0:
                self.move(Vector(0, self.vl))
                self.jumps -= 1
            elif touch.x < (2 * self.left) and self.jumps > 0:
                self.move(Vector(0, -self.vl))
                self.jumps -= 1
        else:
            self.gravity = self.gravity * (-1)

    def move(self, vector):
        self.vector += vector
        if self.vector.length() > 15:
            self.vector = self.vector.normalize() * 10
        if self.ground <= (self.vector[1] + self.y) <= self.ceiling:
            self.pos = self.vector + self.pos
        else:
            self.vector[1] = 0
            self.jumps = 5

    def reset(self):
        self.pos = (50, (Window.height * 0.162))
        self.jumps = 5


class Ground(Widget):
    pass


class Ceiling(Widget):
    pass


class Wall(Widget):
    def __init__(self, **kwargs):
        super(Wall, self).__init__(**kwargs)
        self.vector = Vector(-5, 0)
        self.pos = (Window.width, randint(int(Window.height * 0.13), int((Window.height * 0.87) - self.height)))
        self.size_hint = (randint(50, 200) / Window.width, randint(50, 200) / Window.height)

    def move(self):
        self.pos = self.vector + self.pos

    def __del__(self):
        self.canvas.clear()


class Gravity(App):
    def build(self):
        self.load_kv('main.kv')
        return Game()


if __name__ == '__main__':
    Gravity().run()
