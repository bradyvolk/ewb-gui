"""
Class definition for NLBIdentificationWindow
"""

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import widgets.NLBIdentificationWindowWidget


class NLBIdentificationWindow(Screen):

    def __init__(self, **kwargs):
        super(NLBIdentificationWindow, self).__init__(**kwargs)

