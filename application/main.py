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
from kivy.garden.mapview import MarkerMapLayer
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
import os
import webbrowser 
import kivy
kivy.require('1.0.7')


class HomeWindow(Screen):
    """
    Login screen
    """
    def open_projectinfo(self, weblink):
        webbrowser.open(weblink)
    


class MapWindow(Screen):
    """
    Mapping screen and code for loading maps
    """
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    map_source = ""

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.map_source = path
        self.dismiss_popup()
    
    


class WindowManager(ScreenManager):
    """
    Navigation Router
    """
    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('LoadDialog', cls=LoadDialog)


class DrawableMapView(MapView):
    """
    Garden MapView, but it's drawable
    """
    draw_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        return super().__init__()

    def on_touch_move(self, touch):
        """
        If in draw mode, add map markers wherever touch event is
        """
        if self.draw_mode:
            # Harcoded bias offset for y is concerning
            coord = self.get_latlon_at(touch.x, touch.y - 115, zoom=None)
            marker = MapMarker()
            marker.source = "resources/images/marker.png"
            (marker.lat, marker.lon) = (coord.lat, coord.lon)
            marker.size = (10, 10)
            marker.color = (0.6, 0, 0, 1)  # brown
            self.add_marker(marker)

    def toggle_draw_mode(self):
        """
        Turns on and off draw mode
        """
        self.draw_mode = not self.draw_mode
        self._scatter.do_translation_x = not self._scatter.do_translation_x
        self._scatter.do_translation_y = not self._scatter.do_translation_y

    def clear_paths_drawn(self):
        """
        Clears all paths drawn
        """
        self.remove_layer(self._default_marker_layer)
        self._default_marker_layer = None

    def set_map_source(self):
        """
        Sets the map source for our code
        """
        pass


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
