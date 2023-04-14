"""
Main file for application.

Imports the other windows where most of the action is for our code.

Three Windows as of now:
(1) HomeWindow - home screen of the application
(2) NDVIIndexWindow - NDVI Index Phase of application
(3) MapWindow - Route Planning Phase of application
(4) NLBIdentificationWindow - Identification of NLB Phase of application
(5) InstructionsWindow - windows for instructions on using application

"""

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from windows.HomeWindow import HomeWindow
from windows.RoutePlanningWindow import RoutePlanningWindow
from windows.TrainingWindow import TrainingWindow
from windows.InstructionsWindow import InstructionsWindow
from windows.NDVIIndexWindow import NDVIIndexWindow
from windows.NLBIdentificationWindow import NLBIdentificationWindow
from kivy.clock import Clock

import kivy
kivy.require('1.0.7')

Clock.max_iteration = 20


class WindowManager(ScreenManager):
    """
    Navigation Router
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
