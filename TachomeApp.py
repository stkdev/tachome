from kivy.app import App
from kivy.clock import Clock
from Tachometer import Tachometer
from kivy.core.window import Window

class TachomeApp(App):
    FPS = 30

    def build(self):
        Window.size = (1280, 720)
        Window.clearcolor = (1, 1, 1, 1)
        tachome = Tachometer()
        Clock.schedule_interval(tachome.update, 1.0 / self.FPS)
        Clock.schedule_interval(tachome.update60, 1.0 / (self.FPS / 60))

        return tachome

