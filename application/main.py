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
    line_drawing_mode = BooleanProperty(False)
    start_of_line_segment = None
    # For some reason, up clicks are detected twice so hacky way to prevent that
    alternate = BooleanProperty(False)
    # TODO maybe find a better solution to this

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

    def on_touch_down(self, touch):
        """
        if in draw_mode, place a marker at the touch
        """
        pos = (touch.x, touch.y)
        if self.draw_mode:
            if not self.line_drawing_mode:
                self.add_marker_at_pos(pos, True)
            else:
                self.add_marker_at_pos(pos)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        if in draw_mode, and in line_drawing_mode, place an endpoint for the line
        segment and fill in points in between
        otherwise, if in draw_mode, just change line_drawing_mode to True
        """
        if self.alternate:
            self.alternate = False
            pos = (touch.x, touch.y)
            if self.draw_mode:
                if not self.line_drawing_mode:
                    self.line_drawing_mode = True
                else:
                    start = (self.start_of_line_segment.lat,
                             self.start_of_line_segment.lon)
                    end = self.get_latlon_at(pos[0], pos[1])
                    end = (end.lat, end.lon)
                    self.create_line_segment(start, end)
                    self.start_of_line_segment = pos
                    self.line_drawing_mode = False
        else:
            self.alternate = True
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        """
        """
        pass

    def add_marker_at_pos(self, pos, is_start_of_line_segment=False):
        """
        Adds a marker at pos where pos is a tuple of x and y coordinates
        """
        x = pos[0]
        y = pos[1]
        coord = self.get_latlon_at(x, y)
        marker = MapMarker()
        if is_start_of_line_segment:
            self.start_of_line_segment = marker
        marker.source = "resources/images/marker.png"
        (marker.lat, marker.lon) = (coord.lat, coord.lon)
        marker.size = (10, 10)
        marker.color = (0.6, 0, 0, 1)  # brown
        self.add_marker(marker)

    def add_marker_at_latlon(self, latlon):
        marker = MapMarker()
        marker.source = "resources/images/marker.png"
        (marker.lat, marker.lon) = latlon
        marker.size = (10, 10)
        marker.color = (0.6, 0, 0, 1)  # brown
        self.add_marker(marker)

    def undo(self):
        """
        Removes most recent line segment drawn
        """
        pass

    def create_line_segment(self, start, end, num_points=50):
        """
        Creates a line segment of discrete points with endpoints of start and end
        number of points between line segment determined by num_points
        non-endpoints are added as markers to map
        """
        (start_x, start_y) = start
        (end_x, end_y) = end
        dist_x = end_x - start_x
        dist_y = end_y - start_y
        x_dist_between_points = dist_x / (num_points + 1)
        y_dist_between_points = dist_y / (num_points + 1)

        current_x = start_x
        current_y = start_y
        for i in range(num_points):
            current_x += x_dist_between_points
            current_y += y_dist_between_points
            self.add_marker_at_latlon((current_x, current_y))

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
            self.start_of_line_segment = None
            self.line_drawing_mode = False

    def get_latlon_at(self, x, y, zoom=None):
        """
        Gets lat lon at a given coordinated, calibrated for the offset on our app
        """
        return super().get_latlon_at(x, y - 115, zoom=zoom)

    def set_map_source(self):
        """
        Sets the map source for our code
        """
        # TODO figure out how to change the map out with the insert image button
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
