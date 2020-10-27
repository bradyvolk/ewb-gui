"""
Application built from a  .kv file
"""

from os.path import dirname, join, normpath
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from windows.MapWindow import MapWindow
import os
import webbrowser
import kivy
kivy.require('1.0.7')


class InstructionsWindow(Screen):
    current_instruction = StringProperty()
    instructions = ["step 1", "step 2", "step 3"]
    index = 0

    def __init__(self, **kwargs):
        super(InstructionsWindow, self).__init__(**kwargs)
        self.current_instruction = self.instructions[self.index]

    "Instructions Window"

    def goBack(self):
        if self.index > 0:
            self.index -= 1
        self.current_instruction = self.instructions[self.index]

    def updateInstructions(self):
        if self.index < (len(self.instructions)-1):
            self.index += 1
        self.current_instruction = self.instructions[self.index]


class HomeWindow(Screen):
    """
    Login screen
    """

    def open_documentation(self):
        curdir = dirname(__file__)
        filename = join(curdir, 'resources')
        filename = join(filename, 'pdfs')
        filename = join(filename, 'Electrical%20Build.pdf')
        filename = filename + ""
        filename = filename.replace("\\", "/")
        print(filename)
        webbrowser.open("file:///" + filename)

    def open_projectinfo(self, weblink):
        webbrowser.open(weblink)


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
