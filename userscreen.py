from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen



class UserScreen(Screen):
    """
    UserScreen: ユーザー詳細画面のWidget。
    """
    def __init__(self, **kwargs):
        super(UserScreen, self).__init__(**kwargs)
        icon, userid, vio, akeets = self.get_detail(self.name)

    def get_detail(self, name="aki1502"):
        return "", 0, "", []

    def follow(self, name):
        pass

    def remove(self, name):
        pass



kv = r"""
<UserScreen>:
    Label:
        text: root.name
"""

Builder.load_string(kv)