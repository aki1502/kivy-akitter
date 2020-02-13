from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
import requests

from modules.akeet import Akeet
from modules.user import User
from variables import config, url



class UserScreen(Screen):
    """
    ユーザー詳細画面のWidget。
    """
    icon = StringProperty()
    vio = StringProperty()
    def __init__(self, **kwargs):
        super(UserScreen, self).__init__(**kwargs)
        u = User.fromusername(config.un)
        self.vio = u.vio
        self.icon = u.icon

    def follow(self):
        pass

    def remove(self):
        pass

    def edit(self):
        pass

    def signout(self):
        pass

    def utl(self):
        pass


class UserAkeetColumn(RecycleView):
    """
    ユーザー詳細画面のAkeet欄のWidget。
    """
    def __init__(self, **kwargs):
        super(UserAkeetColumn, self).__init__(**kwargs)
        self.data = self.get_akeets()

    def get_akeets(self):
        """最新のAkeetを取得する。"""
        r = requests.get(url.AKEETS, {"author__username": config.un})
        data = r.json()
        return [Akeet.from_response(r).row() for r in data]



kv = r"""
<UserScreen>:
    font_size: self.width/sp(37) if self.width > 14*sp(37) else self.width/sp(24)

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: "horizontal"
            padding: sp(5), sp(5), sp(5), sp(5)

            Image:
                size_hint: None, None
                height: self.parent.height
                source: root.icon

            BoxLayout:
                orientation: "vertical"

                Label:
                    text: "username: "+root.name
                    font_size: root.font_size
                    text_size: self.size
                    halign: "left"
                    valign: "top"
                    padding_x: sp(10)

                Label:
                    size_hint_y: 2
                    text: "vio: "+root.vio
                    font_size: root.font_size
                    text_size: self.size
                    halign: "left"
                    valign: "top"
                    padding_x: sp(10)

                BoxLayout:
                    orientation: "horizontal"
                    padding: sp(5), 0, 0, 0

                    Button:
                    Button:
                    Button:
            
        UserAkeetColumn:
            viewclass: "AkeetRow"

            size_hint_y: 4

            RecycleBoxLayout:
                default_size: None, root.width/10 if self.width > 14*sp(37) else self.width/6
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
"""

Builder.load_string(kv)