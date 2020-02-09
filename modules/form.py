from kivy.lang.builder import Builder



kv = r"""
<Form@AnchorLayout>:
    label_text: ""
    password: False

    textinput_font_size: 35
    textinput_height: sp(50)
    textinput_width: sp(500)

    text: textinput.text

    BoxLayout:
        orientation: "vertical"
        size_hint_x: None
        width: root.textinput_width

        Label:
            text: root.label_text
            font_size: root.textinput_font_size

        TextInput:
            id: textinput
            size_hint_y: None
            height: root.textinput_height
            font_size: root.textinput_font_size
            multiline: False
            password: root.password
            cursor_color: 0.937, 0.506, 0.059, 0.8 # orange
            selection_color: 0.937, 0.506, 0.059, 0.221 # orange
"""

Builder.load_string(kv)
