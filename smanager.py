from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from akeetform import AkeetForm
from signform import SigninForm, SignupForm
from userscreen import UserScreen


class SManager(ScreenManager):
    """
    SManager: 画面遷移を管理するWidget。
    """
    def __init__(self, **kwargs):
        super(SManager, self).__init__(**kwargs)
        screens = [
            ["menuscreen", MenuScreen],
            ["signinform", SigninForm],
            ["signupform", SignupForm],
        ]
        for name, klass in screens:
            screen = klass(name=name)
            self.add_widget(screen)

    def gtl(self, direction="right"):
        if self.current_screen.name == "gtl":
            return None
        self.clear_widgets()
        self.add_widget(AkeetForm(name="gtl"))
        self.transition.direction = direction
        self.current = "gtl"

    def user(self, name=None):
        name = name or self.parent.name
        if self.current_screen.name == name:
            return None
        self.clear_widgets()
        self.add_widget(UserScreen(name=name))
        self.transition.direction = "left"
        self.current = name

class MenuScreen(Screen):
    pass



kv = r"""
<MenuScreen>:
    Image:
        source: "./images/menu.png"
        size_hint: None, None
        size: root.height*2, root.height
        pos: root.width/2-root.height, 0
"""

Builder.load_string(kv)