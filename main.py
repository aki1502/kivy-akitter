from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

import labar
import smanager
from variables import config


class AkitterApp(App):
    """
    AkitterApp: Akitterのmain app。
    """
    def build(self):
        return AkitterRoot()
        

class AkitterRoot(BoxLayout):
    """
    AkitterRoot: Akitterのroot widget。
    """
    pass



kv = r"""
#:kivy 1.11.1

AkitterRoot:

<AkitterRoot>:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: 0.467, 0.533, 0.600, 1 # lightslategray
        Rectangle:
            pos: self.pos
            size: self.size

    ActionBar:
        LaView:
            id: laview
            use_separator: True

    SManager:
        id: smanager
"""

Builder.load_string(kv)

if __name__ == "__main__":
    app = AkitterApp()
    app.run()
    config.qt = True