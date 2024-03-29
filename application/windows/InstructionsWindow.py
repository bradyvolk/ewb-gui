"""
Class definition for InstructionsWindow
"""

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import widgets.InstructionsWindowWidget


class InstructionsWindow(Screen):
    current_instruction = StringProperty()
    instructions = ["step 1", "step 2", "step 3"]
    index = 0

    def __init__(self, **kwargs):
        super(InstructionsWindow, self).__init__(**kwargs)
        self.current_instruction = self.instructions[self.index]

    "Instructions Window"

    def to_previous_instruction(self):
        """
        Button method that causes screen to go back to previous instruction window
        """
        if self.index > 0:
            self.index -= 1
        self.current_instruction = self.instructions[self.index]

    def to_next_instruction(self):
        """
        Button method that causes screen to go to next instruction
        """
        if self.index < (len(self.instructions)-1):
            self.index += 1
        self.current_instruction = self.instructions[self.index]
