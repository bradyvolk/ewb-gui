'''
Application built from a  .kv file
'''

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapMarker
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

import kivy
kivy.require('1.0.7')


class HomeWindow(Screen):
    """
    Login screen
    """
    pass


class MapWindow(Screen):
    """
    Mapping screen
    """
    pass


class WindowManager(ScreenManager):
    """
    Navigation Router
    """
    pass


class DrawableMapView(MapView):
    """
    Garden MapView, but it's drawable
    """
    draw_mode = False

    def __init__(self, **kwargs):
        return super().__init__()

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.draw_mode:
            # Harcoded bias offset for y is concerning
            coord = self.get_latlon_at(touch.x, touch.y - 115, zoom=None)
            marker = MapMarker()
            (marker.lat, marker.lon) = (coord.lat, coord.lon)
            marker.size = (20, 20)
            marker.color = (1, 0, 0, 1)
            self.add_marker(marker)

    def do_update(self, dt):
        if not self.draw_mode:
            print("updating")
            super().do_update(dt)

    def on_transform(self, *args):
        if not self.draw_mode:
            super().on_transform(*args)


# Sets file to load
main_file = Builder.load_file("main.kv")


class MyMainApp(App):
    """
    Main App Class Defintion
    """

    def build(self):
        """
        Currently just returns main_file which holds the whole app
        """
        return main_file


# Main Loop
if __name__ == "__main__":
    MyMainApp().run()
