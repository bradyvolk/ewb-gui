"""
Design of HomeWindow screen in Kv langauge
"""


from kivy.lang import Builder

Builder.load_string("""
<HomeWindow>:
    name: "home_window"

    # Video:
    #    source: "resources/images/test.avi"
    #    pos: self.pos
    #    size: self.size

    GridLayout:
        rows: 2
        columns: 1
        padding: 100
        spacing: 100
        orientation: "tb-lr"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "resources/images/light-green.jpg"
        # Title
        Label:
            size_hint: (1, 0.2)
            text: "Digital Agriculture"
            font_size: 60
            font_name: "resources/fonts/Orbitron-Bold.ttf"
            bold: True
            color: (240, 240, 240, 1)
        
        # Navigation Buttons
        GridLayout:
            col: 1
            rows: 5
            spacing: 10
            Button:
                text: "Phase 1: NDVI Index"
                on_release: 
                    app.root.current = "ndvi_index_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Phase 2: Route Planning"
                on_release: 
                    app.root.current = "route_planning_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Phase 3: Identify NLB"
                on_release:
                    app.root.current = "nlb_identification_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Instructions"
                on_release:
                    app.root.current = "instructions_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Project Information"
                on_release:
                    root.open_projectinfo("https://ewb.engineering.cornell.edu/subteams.html")
            
""")
