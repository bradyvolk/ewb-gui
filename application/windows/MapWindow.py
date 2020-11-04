"""
Contains definition for MapWindow classes
and all of the functionality contained
within the map_window screen of our application
"""

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapMarker
from kivy.garden.mapview import MarkerMapLayer
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
import widgets.MapWindowWidget


class MapWindow(Screen):
    """
    Mapping screen and code for loading maps
    """
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    map_source = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    # TODO maybe find a better solution to this
    alternate = BooleanProperty(False)

    bottom_of_map = 0
    top_of_map = 0
    line_segments = []

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
        self.calculate_top_and_bottom_of_map()
        pos = (touch.x, touch.y)
        # make sure in draw mode, mouse isn't scrolling, and touch is actually on map
        if self.draw_mode and not touch.is_mouse_scrolling and self.is_touch_on_map(touch):
            if not self.line_drawing_mode:
                self.add_marker_at_pos(pos, True)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        if in draw_mode, and in line_drawing_mode, place an endpoint for the line
        segment and fill in points in between
        otherwise, if in draw_mode, just change line_drawing_mode to True
        """
        # mouse isn't scrolling and touch is actually on map
        if not touch.is_mouse_scrolling and self.is_touch_on_map(touch):
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
        Adds a marker at pos where pos is a tuple of x and y pixel values
        """
        x = pos[0]
        y = pos[1]
        coord = self.get_latlon_at(x, y)
        marker = MapMarker()
        if is_start_of_line_segment:
            self.start_of_line_segment = marker
            self.line_segments.append([])
        marker.source = "resources/images/marker.png"
        (marker.lat, marker.lon) = (coord.lat, coord.lon)
        marker.size = (10, 10)
        marker.color = (0.6, 0, 0, 1)  # brown
        self.line_segments[len(self.line_segments)-1].append(marker)
        self.add_marker(marker)

    def add_marker_at_latlon(self, latlon):
        marker = MapMarker()
        marker.source = "resources/images/marker.png"
        (marker.lat, marker.lon) = latlon
        marker.size = (10, 10)
        marker.color = (0.6, 0, 0, 1)  # brown
        self.line_segments[len(self.line_segments)-1].append(marker)
        self.add_marker(marker)

    def undo(self):
        """
        Removes most recent line segment drawn
        """
        if not self.line_segments:
            return
        most_recent_line_segment = self.line_segments[len(
            self.line_segments) - 1]
        if len(most_recent_line_segment) == 1:
            self.start_of_line_segment = None
            self.line_drawing_mode = False
        for marker in most_recent_line_segment:
            self.remove_marker(marker)
        self.line_segments = self.line_segments[0:len(self.line_segments) - 1]

    def create_line_segment(self, start, end, num_points=20):
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
        for i in range(num_points + 1):
            current_x += x_dist_between_points
            current_y += y_dist_between_points
            self.add_marker_at_latlon((current_x, current_y))

    def create_line_segment_with_fixed_distance(self, start, end):
        """
        # TODO This does not work yet. Ultimately, we want to 
        set the distance between GPS markers to be fixed, i.e. not
        based on distance between the two points in any sense or based
        on the zoom of the user
        """
        # TODO need to determine lat and lon intervals by a switch-like statement
        (lat_interval, lon_interval) = (0.01, 0.01)
        (start_lat, start_lon) = start
        (end_lat, end_lon) = end
        dist_lat = end_lat - start_lat
        dist_lon = end_lon - start_lon
        slope = (dist_lon / dist_lat)
        lat_interval = lat_interval*(-1) if dist_lat < 0 else lat_interval
        lon_interval = lon_interval*(-1) if dist_lon < 0 else lon_interval

        lon_interval = lon_interval * slope

        current_lat = start_lat
        current_lon = start_lon
        while current_lat >= end_lat:
            current_lat += lat_interval
            current_lon += lon_interval
            self.add_marker_at_latlon((current_lat, current_lon))

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
            self.line_segments = []

    def get_latlon_at(self, x, y, zoom=None):
        """
        Gets lat lon at a given coordinated, calibrated for the offset on our app
        """
        return super().get_latlon_at(x, y - 115, zoom=zoom)

    def is_touch_on_map(self, touch):
        """
        determines if touch is on visible portion of map
        """
        return touch.y >= self.bottom_of_map and touch.y <= self.top_of_map

    def calculate_top_and_bottom_of_map(self):
        """
        Calculates top and bottom of map
        """
        app = App.get_running_app()
        map_window_ids = app.root.children[0].ids
        title_FloatLayout = map_window_ids["title_FloatLayout"]
        drawing_tools_GridLayout = map_window_ids["drawing_tools_GridLayout"]
        self.top_of_map = title_FloatLayout.center_y - \
            (title_FloatLayout.height / 2)
        self.bottom_of_map = drawing_tools_GridLayout.center_y + \
            (drawing_tools_GridLayout.height / 2)

    def run_path(self):
        """
        Constructs and returns list of coordinates to send to Rover
        """
        coords = []
        for paths in self.line_segments:
            for marker in paths:
                coords.append((marker.lat, marker.lon))
        return coords

    def set_map_source(self):
        """
        Sets the map source for our code
        """
        # TODO figure out how to change the map out with the insert image button
        pass
