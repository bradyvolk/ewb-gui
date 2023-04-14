"""
Class definition for NDVIIndexWindow
"""

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import widgets.NDVIIndexWindowWidget


class NDVIIndexWindow(Screen):

    def __init__(self, **kwargs):
        super(NDVIIndexWindow, self).__init__(**kwargs)

