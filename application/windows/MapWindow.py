"""
Contains definition for MapWindow classes
and all of the functionality contained
within the map_window screen of our application
"""

from os.path import join, dirname, abspath
from itertools import takewhile
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.garden.mapview import MapView
from kivy.garden.mapview import MapMarker
from kivy.garden.mapview import MarkerMapLayer
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.scatter import Scatter
from kivy.graphics import Color
from kivy.graphics import Line
import widgets.MapWindowWidget
from Pixel_to_GPS import pixel_to_GPS


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
        """
        Shows the pop up for the kivy file explorer
        """
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """
        Loads file from file explorer in kivy when uploading image to 
        be used for a map.
        """
        self.map_source = filename[0]
        self.dismiss_popup()
        self.coord_dialog = CoordinateDialog(
            submit_coordinates=self.submit_coordinates, cancel=self.dismiss_popup)
        self._popup = Popup(title="Input Coordinates", content=self.coord_dialog,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def submit_coordinates(self):
        """
        Checks if user inputted at least 3 valid coordinates and send them to 
        our DrawableMapView if so.
        """
        (tl_coord, tr_coord, bl_coord, br_coord) = self.validate_coordinates()
        coords = [tl_coord, tr_coord, bl_coord, br_coord]

        if coords.count(None) > 1:
            print("here")
            print(coords)
            pass
        else:
            self.dismiss_popup()
            self.ids["map"].load_map_source(
                self.map_source, tl_coord, tr_coord, bl_coord, br_coord)

    def validate_coordinates(self):
        """
        Validates user-inputted coordinates
        """
        coord_ids = ["tl_coord", "tr_coord", "bl_coord", "br_coord"]
        (tl_coord, tr_coord, bl_coord, br_coord) = (None, None, None, None)
        coords = [tl_coord, tr_coord, bl_coord, br_coord]

        for i in range(len(coord_ids)):
            coords[i] = self.validate_coordinate(coord_ids[i])

        return coords

    def validate_coordinate(self, coord_id):
        """
        Validates a given user-inputted coordinate. If the input is 
        non-numeric, then the label is given an (Invalid) marker, and
        the text changes to red to indicate to the user the invalid input.
        """
        label_id = coord_id + "_label"
        label = self.coord_dialog.ids[label_id]
        try:
            coord = float(self.coord_dialog.ids[coord_id].text)
            if "(Invalid)" in label.text:
                label.text = label.text[:label.text.find(" (Invalid)")]
            label.color = (1, 1, 1, 1)
        except:
            coord = None
            if "(Invalid)" not in label.text:
                label.text = label.text + " (Invalid)"
            label.color = (1, 0, 0, 0.8)
        return coord


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class CoordinateDialog(FloatLayout):
    submit_coordinates = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('CoordinateDialog', cls=CoordinateDialog)


class DrawableMapView(Scatter):
    """
    Main MapView on which we will put our images
    and where we will draw
    """
    lines = []
    first_position = None
    draw_mode = False
    image_uploaded = False
    pixel_to_GPS_map = None

    def __init__(self, **kwargs):
        self.do_rotation = False
        self.do_translation = (False, False)
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        """
        When in draw_mode (TODO), make a line segment
        path based on current touch and last touch
        """
        if self.draw_mode and self.image_uploaded:
            x = touch.x
            y = touch.y
            (abs_x, abs_y) = self.to_local(x, y)
            with self.canvas:
                Color(0, 0, 0, 1, mode='rgba')  # black
                # Three cases:
                # Case 1: no touches yet, so mark where first touch is
                if not self.first_position:
                    self.first_position = (abs_x, abs_y)
                else:
                    # Case 2: one touch so far, with this next touch make a line
                    # segment from first_position touch and current touch
                    if not self.lines:
                        start_x = self.first_position[0]
                        start_y = self.first_position[1]
                        end_x = abs_x
                        end_y = abs_y
                        self.lines.append(
                            Line(points=[start_x, start_y, end_x, end_y], width=5))
                    # Case 3: there are already line segments, so make a new line segment
                    # from our last made line segment's last endpoints and our current touch
                    else:
                        last_line = self.lines[len(self.lines)-1]
                        start_x = last_line.points[len(last_line.points)-2]
                        start_y = last_line.points[len(last_line.points)-1]
                        end_x = abs_x
                        end_y = abs_y
                        self.lines.append(
                            Line(points=[start_x, start_y, end_x, end_y], width=5))
        super().on_touch_down(touch)

    def toggle_draw_mode(self):
        """
        Turns on and off self.draw_mode
        """
        self.draw_mode = not self.draw_mode
        self.do_translation_x = not self.do_translation_x
        self.do_translation_y = not self.do_translation_y

    def undo(self):
        """
        Removes the last drawn line
        """
        with self.canvas:
            if self.lines:
                line = self.lines.pop()
                self.canvas.remove(line)
                if not self.lines:
                    self.first_position = None

    def clear(self):
        """
        Removes all drawn lines
        """
        self.lines = []
        self.first_position = None
        with self.canvas:
            for child in self.canvas.children:
                if type(child) == Line:
                    self.canvas.remove(child)

    def recenter(self):
        """
        Recenters and rescales the image
        """
        self.scale = 1
        self.x = 0
        self.y = 0

    def load_map_source(self, map_source, tl_coord, tr_coord, bl_coord, br_coord):
        """
        Changes the DrawableMapView to use the uploaded map_source image,
        and uses the inputted coordinates to create a map from pixel to GPS
        coordinates.
        """
        # Changing the canvas, visual stuff
        self.canvas.clear()
        self.do_translation = (True, True)
        self.image_uploaded = True
        for child in self.parent.parent.children:
            if type(child) == Label:
                self.parent.parent.remove_widget(child)
        self.add_widget(Image(source=map_source, size=self.size, pos=self.pos))

        # Creating our pixel to GPS map
        # self.pixel_to_GPS_map = pixel_to_GPS()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('LoadDialog', cls=LoadDialog)
