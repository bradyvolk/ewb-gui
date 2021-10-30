"""
Class definition for HomeWindow
"""

from kivy.uix.screenmanager import Screen
import os
import webbrowser
import widgets.DetectWindowWidget
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
import os


class DetectWindow(Screen):
    """
    Window for drone image processing
    """

    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    path_to_training_set = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        """
        Shows the pop up for the kivy file explorer
        """
        content = LoadDialog(
            load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """
        Loads file from file explorer in kivy when uploading image to
        be used for a map.
        """
        if filename == []:  # this means a file was NOT selected
            self.path_to_image_set = path
            print(path)
            print(self.path_to_image_set)
            self.dismiss_popup()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('LoadDialogDetect', cls=LoadDialog)
