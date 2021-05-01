import psutil

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.scatter import Scatter
import datetime
import os

class Picture(Scatter):

    source = StringProperty(None)
    size = ObjectProperty(None)
    angle = NumericProperty(0)

    def __init__(self, source, size=(100, 100), center=(100, 100), angle=0):
        super().__init__()

        self.source = source
        self.size = size
        self.center = center
        self.angle = angle


class Tachometer(Widget):
    bg_img = ObjectProperty(None)
    cpu = ObjectProperty(None)
    time = StringProperty('')
    temperature = StringProperty('')
    trip = StringProperty('')
    trip_cons = StringProperty('')
    voltage = StringProperty('')
    # mv_img = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.images = self.init_image()
        self.add_images()

    def init_image(self):
        ret = {
            # "back": Picture(source='img/m_back.png', size=(550, 550), center=(500, 300)),
            "hari": Picture(source='img/m_hari.png', size=(530, 530), center=(500, 300)),
            "maru": Picture(source='img/m_maru.png', size=(150, 150), center=(500, 300), angle=0),
        }

        return ret

    def add_images(self):
        # for key in ["waku"]:
        #     self.add_widget(self.images[key])
        for key, img in self.images.items():
            self.add_widget(img, index=1)

    def update_cpu(self, base, w):
        if base is None:
            base = 0

        cpu_now = psutil.cpu_percent(interval=1/60)
        return (base * (w-1) + cpu_now) / w

    def update_image_pos(self):
        # self.images["back"].center_x = Window.size[0] / 3 * 2
        # self.images["back"].size = (Window.size[0], Window.size[1])
        bg_size = self.ids.bg_img.size
        if bg_size[0] < 16/9*bg_size[1]:
            bg_size = (bg_size[0], int(bg_size[0]*9/16))
        else:
            bg_size = (int(bg_size[1]*16/9), bg_size[1])

        self.images["hari"].center_x = self.ids.bg_img.center[0] + bg_size[0]/8
        self.images["hari"].center_y = self.ids.bg_img.center[1]
        self.images["hari"].size = (bg_size[1]*0.8,bg_size[1]*0.8)

        self.images["maru"].center_x = self.ids.bg_img.center[0] + bg_size[0]/8
        self.images["maru"].center_y = self.ids.bg_img.center[1]
        self.images["maru"].size = (bg_size[0]*0.2, bg_size[1]*0.2)
        self.voltage = "%s,%s" % bg_size

    def update(self, dt):
        dt_now = datetime.datetime.now()
        if dt_now.second % 2 == 0:
            self.time = dt_now.strftime('%H:%M:%S')
        else:
            self.time = dt_now.strftime('%H:%M:%S')
        self.cpu = round(self.update_cpu(self.cpu, 30), 1)
        self.images["hari"].angle = -15-self.cpu*5

        bg = self.ids.bg_img
        self.trip = str(bg.width)
        self.trip_cons = str(bg.height)

        self.update_image_pos()

    def update60(self, dt):
        if os.name == "nt":
            self.temperature = "-"
        else:
            self.temperature = str(psutil.sensors_temperatures(False)["cpu_thermal"][0].current)

