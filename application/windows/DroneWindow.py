"""
Class definition for HomeWindow
"""

from kivy.uix.screenmanager import Screen
import os
import webbrowser
import widgets.DroneWindowWidget
from os.path import dirname, join, normpath
from itertools import takewhile
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.image import Image
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


class DroneWindow(Screen):
    """
    Window for drone image processing
    """

    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    img_source = None

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
        (bl_coord_lat, bl_coord_lon, tl_coord_lat, tl_coord_lon, br_coord_lat,
         br_coord_lon, tr_coord_lat, tr_coord_lon) = self.validate_coordinates()

        coords = [(bl_coord_lat, bl_coord_lon), (tl_coord_lat, tl_coord_lon),
                  (br_coord_lat, br_coord_lon), (tr_coord_lat, tr_coord_lon)]

        invalidpairs = 0

        for (lat, lon) in coords:
            if lat == None or lon == None:
                invalidpairs += 1

        if invalidpairs > 1:
            pass
        else:
            self.dismiss_popup()
            self.ids["map"].load_map_source(
                self.map_source, coords)

    def validate_coordinates(self):
        """
        Validates user-inputted coordinates
        """
        coord_ids = ["bl_coord_lat", "bl_coord_lon", "tl_coord_lat", "tl_coord_lon",
                     "br_coord_lat", "br_coord_lon", "tr_coord_lat", "tr_coord_lon"]
        (bl_coord_lat, bl_coord_lon, tl_coord_lat, tl_coord_lon, br_coord_lat,
         br_coord_lon, tr_coord_lat, tr_coord_lon) = (None, None, None, None, None, None, None, None)
        coords = [bl_coord_lat, bl_coord_lon, tl_coord_lat, tl_coord_lon, br_coord_lat,
                  br_coord_lon, tr_coord_lat, tr_coord_lon]

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
