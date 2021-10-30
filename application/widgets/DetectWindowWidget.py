"""
Design of DetectWindow screen in Kv langauge
"""


from kivy.lang import Builder

Builder.load_string("""
<DetectWindow>:
    name: "detect_window"

    AnchorLayout:
        id: map_window_AnchorLayout
        anchor_y: "top"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "resources/images/dark-grey.jpg"
                
        # Back Button and Title
        FloatLayout:
            id: title_FloatLayout
            size_hint_y: 0.1
            canvas.before:
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: "resources/images/dark-grey.jpg"
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
                text: "Detect NLB with rCNN"
                font_size: 30
                font_name: "resources/fonts/Orbitron-Bold.ttf"
                bold: True
                color: "#C0C0C0"

        AnchorLayout:
            anchor_y: "bottom"
            BoxLayout:
                orientation: "horizontal"
                Button:
                    text: "Upload Images"
                    size_hint: (0.5, 0.1)
                    on_release: 
                        print(root.ids);
                        root.show_load()
                Button:
                    text: "Detect"
                    size_hint: (0.5, 0.1)
                    on_release: root.show_load()
                    
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
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
