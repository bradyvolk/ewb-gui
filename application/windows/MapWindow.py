"""
Contains definition for MapWindow classes
and all of the functionality contained
within the map_window screen of our application
"""

from os.path import join, dirname
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


class MapLayer(Widget):
    """A map layer, that is repositionned everytime the :class:`MapView` is
    moved.
    """
    viewport_x = NumericProperty(0)
    viewport_y = NumericProperty(0)

    def reposition(self):
        """Function called when :class:`MapView` is moved. You must recalculate
        the position of your children.
        """
        pass

    def unload(self):
        """Called when the view want to completly unload the layer.
        """
        pass


class MarkerMapLayer(MapLayer):
    """A map layer for :class:`MapMarker`
    """
    order_marker_by_latitude = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.markers = []
        super(MarkerMapLayer, self).__init__(**kwargs)

    def insert_marker(self, marker, **kwargs):
        if self.order_marker_by_latitude:
            before = list(takewhile(
                lambda i_m: i_m[1].lat < marker.lat,
                enumerate(self.children)
            ))
            if before:
                kwargs['index'] = before[-1][0] + 1

        super(MarkerMapLayer, self).add_widget(marker, **kwargs)

    def add_widget(self, marker):
        marker._layer = self
        self.markers.append(marker)
        self.insert_marker(marker)

    def remove_widget(self, marker):
        marker._layer = None
        if marker in self.markers:
            self.markers.remove(marker)
        super(MarkerMapLayer, self).remove_widget(marker)

    def reposition(self):
        if not self.markers:
            return
        mapview = self.parent
        set_marker_position = self.set_marker_position
        bbox = None
        # reposition the markers depending the latitude
        markers = sorted(self.markers, key=lambda x: -x.lat)
        margin = max((max(marker.size) for marker in markers))
        bbox = mapview.get_bbox(margin)
        for marker in markers:
            if bbox.collide(marker.lat, marker.lon):
                set_marker_position(mapview, marker)
                if not marker.parent:
                    self.insert_marker(marker)
            else:
                super(MarkerMapLayer, self).remove_widget(marker)

    def set_marker_position(self, mapview, marker):
        x, y = mapview.get_window_xy_from(marker.lat, marker.lon, mapview.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)

    def unload(self):
        self.clear_widgets()
        del self.markers[:]


class DrawableMapView(Scatter):
    """
    Main MapView on which we will put our images
    and where we will draw
    """

    def __init__(self, **kwargs):
        self.do_rotation = False
        self.zoom = self.scale
        self._default_marker_layer = None
        self._layers = []
        self.canvas = Canvas()
        with self.canvas:
            self.canvas_map = Canvas()
            self.canvas_layers = Canvas()
        with self.canvas:
            self.canvas_layers_out = Canvas()
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        absolute_pos = self.to_local(x, y)
        print(absolute_pos)
        print(x, y)
        with self.canvas:
            Color(0, 0, 1, 1, mode='rgba')
            self.rect = Rectangle(
                pos=(absolute_pos[0], absolute_pos[1]), size=(50, 50))
        super().on_touch_down(touch)

    # def on_translation(self, touch):
    #     x = touch.x
    #     y = touch.y
    #     print(x, y)
    #     with self.canvas:
    #         Color(1, 0, 0, 0.5, mode='rgba')
    #         self.rect = Rectangle(pos=(touch.x, touch.y), size=(50, 50))
    #     super().on_translation(touch)

    def collide_point(self, x, y):
        # print "collide_point", x, y
        return True


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('LoadDialog', cls=LoadDialog)
