from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from akeetform import AkeetForm
from signform import SigninForm, SignupForm
from userscreen import UserScreen
from data.loginfo import getloginfo
from variables import config


class SManager(ScreenManager):
    """
    画面遷移を管理するWidget。
    """
    def __init__(self, **kwargs):
        super(SManager, self).__init__(**kwargs)
        if getloginfo()["auth_token"]:
            self.gtl(direction="left")
        else:
            self.unsigned()

    def unsigned(self):
        """サインイン情報がない場合のScreensを構築。"""
        self.clear_widgets()
        screens = [
            ["menuscreen", MenuScreen],
            ["signinform", SigninForm],
            ["signupform", SignupForm],
        ]
        for name, klass in screens:
            screen = klass(name=name)
            self.add_widget(screen)
        self.transition.direction = "right"
        self.current = "menuscreen"

    def gtl(self, direction="right"):
        """global timelineのScreenを構築。"""
        if getattr(self.current_screen, "name", "") == "gtl":
            return None
        self.clear_widgets()
        self.add_widget(AkeetForm(name="gtl"))
        self.transition.direction = direction
        self.current = "gtl"

    def user(self, name=None):
        """ユーザー画面のScreenを構築。"""
        name = name or getloginfo()["username"]
        if self.current_screen.name == name:
            return None
        self.clear_widgets()
        config.qt = True
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