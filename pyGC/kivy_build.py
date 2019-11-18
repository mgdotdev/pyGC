"""
build file for the Kivy builder called in GUI - find it's easier to use a .py
file to script and then call the KVlang variable to build locally.

"""

KVlang = '''

<Meta>:
    orientation: 'vertical'
    rows: 3

<graph_options>:
    id: graph_popup
    title: 'Graph Options'
    size_hint_y: 0.37
    pos_hint: {'top': 0.37}
    background_color: (0, 0, 0, 0)
    BoxLayout:
        GridLayout:
            rows: 3
            cols: 3
            size_hint_x: 2
            Button:
                text: 'Expand U/D'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Up'
                on_press: root.update_graph(self.text)            
            Button:
                text: 'Contract U/D'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Left'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Center'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Right'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Expand L/R'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Down'
                on_press: root.update_graph(self.text)
            Button:
                text: 'Contract L/R'
                on_press: root.update_graph(self.text)

        BoxLayout:
            rows: 4
            size_hint_x: 0.35
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: ''
                    size_hint_y: 0.2

                Label:
                    size_hint_y: 0.2
                    text: str(int(sensitivity.value))                

                Slider:
                    id: sensitivity
                    size_hint_y: 1
                    value: 1
                    min: 0
                    max: 10
                    step: 1
                    orientation: 'vertical'

                Label:
                    text: ''
                    size_hint_y: 0.2

        BoxLayout:
            Label:
                pos_hint: {'center_x': .5, 'center_y': .5}
                text: 'Sensitivity'
                canvas.before:
                    PushMatrix
                    Rotate:
                        angle: 270
                        origin: self.center
                canvas.after:
                    PopMatrix        


            BoxLayout:
                size_hint_x: 3
                Label:
                    text: ''

            BoxLayout:
                size_hint_x: 9
                spacing: 10
                padding: 10
                orientation: 'vertical'

                Button:
                    background_color: (0,0,1,1)
                    text: 'Export graph to Image'
                    on_release: root.save_fig()

                Button:
                    background_color: (0,1,0,1)
                    text: 'Export data to Excel'
                    on_release: root.export_to_excel_trs()

                Button:
                    background_color: (1,0,0,1)
                    text: 'Return'
                    on_release: root.dismiss()

<file_popup>:
    title: 'File Directory'

<help_popup>:
    id: help_popup
    title: 'Help Menu'
    BoxLayout:
        padding: 5
        BoxLayout:
            spacing: 5
            orientation: 'vertical'
            size_hint_x: 0.18
            Button:
                text: "Input Data"
                on_press: root.help_text("Input Data")

            Button:
                text: "Input Graph"
                on_press: root.help_text("Input Graph")

            Button:
                text: "Function Type"
                on_press: root.help_text("Function Type")

            Button:
                text: "Output Graph"
                on_press: root.help_text("Output Graph")

            Button:
                text: "Output Data"
                on_press: root.help_text("Output Data")

            Button:
                text: "About/Contact"
                on_press: root.help_text("About")

            Button:
                text: "Acknowledgments"
                on_press: root.help_text("Acknowledgments")

        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            padding: 10
            ScrollView:
                Label:
                    id: label
                    text: 'Click on the various buttons to the left for explanations to the various functions available in this program.'
                    size_hint_y: None
                    text_size: self.width, None
                    height: self.texture_size[1]
                    font_size: 22

            BoxLayout:
                size_hint_y: 0.15
                Label:
                    size_hint_x: 3
                    text: ''
                Button:              
                    background_color: (1,0,0,1)
                    pos_hint: {"right":1, "bottom":0.5}
                    text: "Return to Main Menu"
                    on_press: root.dismiss()
                    on_release: root.help_text("Done")


<Body>:
    padding: 5
    size_hint_y: 0.5
    rows: 1
    GridLayout:
        size: root.width, root.height
        rows: 4
        orientation: 'vertical'
        BoxLayout:
            Button:
                text: 'Import Data'
                on_release: root.file_popup()   

        BoxLayout:
            Spinner:
                id: condition
                text: 'Function Type: Symmetric Gaussian'
                values: ['Function Type: Symmetric Gaussian', 'Function Type: Asymmetric Gaussian']

        BoxLayout:
            Button:
                text: 'Reset'
                on_release: root.reset_app()
                on_release: condition.text = 'Function Type: Symmetric Gaussian'

            Button:
                text: 'Start'
                background_color: (0,0,1,1)
                on_release: root.calc()

            Button:
                text: 'Help'
                on_release: root.help_popup()
'''
