"""
Contains template rules for MapWindow in kv language
"""

from kivy.lang import Builder

Builder.load_string("""
<MapWindow>:
    name: "map_window"
    GridLayout:
        id: window_grid
        rows: 3
        columns: 10
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "resources/images/dark-grey.jpg"

        # Back Button and Title
        FloatLayout:
            id: title_FloatLayout
            size_hint_y: 0.2
            Button:
                pos_hint: {"x": 0.02, "center_y": 0.5}
                size_hint: (0.1, 0.8)
                text: "Home"
                on_release: 
                    app.root.current = "home_window"
                    root.manager.transition.direction = "right"
            Label:
                pos_hint: {"center_x": 0.5, "center_y":0.5}
                size_hint: (0.8, 0.8)
                text: "Route Planning"
                font_size: 30
                font_name: "resources/fonts/Orbitron-Bold.ttf"
                bold: True
                color: "#C0C0C0"

        # Main Box that contains Map
        BoxLayout:
            id: map_container
            orientation: "horizontal"
            size_hint_y: 2
            AnchorLayout:
                id: map_anchor 
                achor_y: "bottom"  
                FloatLayout:  
                    DrawableMapView:
                        pos_hint: {'top': 1, 'bottom': 1}
                        id: map
                        canvas:
                            Rectangle:
                                source: 'resources/images/tanzania_drone_pic2.jpg'
                                size: self.size
                    # Image:
                    #     id: draw_image
                    #     source: "resources/images/marker.png"
                    #     size_hint: (0.03, 0.03)
                    #     allow_stretch: True
                    #     opacity: 0

        # Map Drawing Tools
        GridLayout:
            id: drawing_tools_GridLayout
            name: "drawing_tools"
            size_hint_y: 0.5
            cols: 2
            padding: 20
            GridLayout:
                cols: 6
                size_hint_y: 0.3
                size_hint_x: 1
                AnchorLayout:
                    Button:
                        text: "Insert Image"
                        size_hint: (1, 0.6)
                AnchorLayout:
                    Button:
                        text: "Undo"
                        size_hint: (1, 0.6)
                        padding_x: 10
                AnchorLayout:
                    Button:
                        text: "Clear"
                        size_hint: (1, 0.6)
                        padding_x: 10
                AnchorLayout:
                    Button:
                        text: "Polygon"
                        size_hint: (1, 0.6)
                        padding_x: 10
                AnchorLayout:
                    Button:
                        text: "Lasso"
                        size_hint: (1, 0.6)
                        padding_x: 10
                AnchorLayout:
                    Button:
                        id: draw_mode_button
                        text: "Draw Path"
                        size_hint: (1, 0.6)
                        padding_x: 10
            AnchorLayout:
                anchor_x: "right"
                size_hint_x: 0.3
                padding: 10
                Button:
                    text: "Run"
                    size_hint: (1, 1)

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            path: "../../../"
            rootpath: "../"
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)
""")
