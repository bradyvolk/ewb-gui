'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

from kivy.uix.button import Button
from kivy.app import App
import kivy
kivy.require('1.0.7')


class TestApp(App):

    def build(self):
        # return a Button() as a root widget
        return Button(text='hello world')


if __name__ == '__main__':
    TestApp().run()
