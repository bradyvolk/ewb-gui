'''
Application built from a  .kv file
'''

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def on_mouse_pos(self, instance, pos):
    #     print(pos)

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
    erase_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self.on_mouse_pos)
        return super().__init__()

    def on_mouse_pos(self, instance, pos):
        """
        Used to set position for drawing and erasing labels
        when the user is in those modes
        """
        (x, y) = pos
        app = App.get_running_app()
        map_window_ids = app.root.children[0].ids
        if self.draw_mode:
            draw_image = map_window_ids["draw_image"]
            draw_image.center_x = x
            draw_image.center_y = y
        if self.erase_mode:
            eraser_image = map_window_ids["eraser_image"]
            eraser_image.center_x = x
            eraser_image.center_y = y

    def on_touch_move(self, touch):
        """
        If in draw mode, add map markers wherever touch event is
        If in erase mode, remove markers wherever touch event is
        """
        # TODO Somehow remove based on marker pixel location instead of coordinate
        # this is too slow, especially when there are a lot of markers

        # TODO break this into some functions probably
        if self.draw_mode:
            # TODO Harcoded bias offset for y is concerning
            coord = self.get_latlon_at(touch.x, touch.y - 115, zoom=None)
            marker = MapMarker()
            marker.source = "resources/images/marker.png"
            (marker.lat, marker.lon) = (coord.lat, coord.lon)
            marker.size = (10, 10)
            marker.color = (0.6, 0, 0, 1)  # brown
            self.add_marker(marker)
        elif self.erase_mode:
            coord = self.get_latlon_at(touch.x, touch.y - 115, zoom=None)
            erase_location = (coord.lat, coord.lon)
            if self._default_marker_layer is not None:
                markers = self._default_marker_layer.markers
                lats = [marker.lat for marker in markers]
                lons = [marker.lon for marker in markers]
                i = 0
                while i < len(lats):
                    print((1 / self._zoom)**6)
                    within_lat = lats[i] <= erase_location[0] + \
                        6000 * \
                        (1 / self._zoom)**6 and lats[i] >= erase_location[0] - \
                        6000 * (1 / self._zoom)**6
                    within_lon = lons[i] <= erase_location[1] + \
                        6000 * \
                        (1 / self._zoom)**6 and lons[i] >= erase_location[1] - \
                        6000 * (1 / self._zoom)**6
                    if within_lat and within_lon:
                        self.remove_marker(markers[i])
                        del lats[i], lons[i]
                    else:
                        i += 1

    def toggle_draw_mode(self):
        """
        Turns on and off draw mode
        """
        self.draw_mode = not self.draw_mode
        app = App.get_running_app()
        map_window_ids = app.root.children[0].ids
        draw_mode_button = map_window_ids["draw_mode_button"]
        draw_image = map_window_ids["draw_image"]
        if self.draw_mode:
            draw_mode_button.background_color = (0.5, 0.5, 0.5, 1)
            draw_image.opacity = 1
        else:
            draw_mode_button.background_color = (1, 1, 1, 1)
            draw_image.opacity = 0
        if self.draw_mode and self.erase_mode:
            self.toggle_erase_mode()
        self.toggle_translation()

    def toggle_erase_mode(self):
        """
        Turns on and off erase mode
        """
        self.erase_mode = not self.erase_mode
        app = App.get_running_app()
        map_window_ids = app.root.children[0].ids
        erase_mode_button = map_window_ids["erase_mode_button"]
        eraser_image = map_window_ids["eraser_image"]
        if self.erase_mode:
            erase_mode_button.background_color = (0.5, 0.5, 0.5, 1)
            eraser_image.opacity = 1
        else:
            erase_mode_button.background_color = (1, 1, 1, 1)
            eraser_image.opacity = 0
        if self.erase_mode and self.draw_mode:
            self.toggle_draw_mode()
        self.toggle_translation()

    def toggle_translation(self):
        """
        Turns on and off map translation
        """
        self._scatter.do_translation_x = not self._scatter.do_translation_x
        self._scatter.do_translation_y = not self._scatter.do_translation_y

    def clear_paths_drawn(self):
        """
        Clears all paths drawn
        """
        if self._default_marker_layer:
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
