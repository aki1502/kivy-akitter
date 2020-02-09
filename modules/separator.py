from kivy.lang.builder import Builder

kv = r"""
<Separator@Widget>:
    size_hint_y: None
    height: sp(1)
    color: 0.467, 0.533, 0.600 # lightslategray
    canvas:
        Color:
            rgb: self.color or (0.467, 0.533, 0.600)
        Rectangle:
            pos: self.pos
            size: self.size
"""

Builder.load_string(kv)