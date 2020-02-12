from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.actionbar import ActionButton, ActionPrevious, ActionView

from data.loginfo import getloginfo



class LaView(ActionView):
    """
    ActionBar直下に置くWidget。
    """
    def __init__(self, **kwargs):
        super(LaView, self).__init__(**kwargs)
        self.add_widget(LaPrevious(fname="menu"))
        if getloginfo()["auth_token"]:
            self.signed()
        else:
            self.unsigned()

    def unsigned(self):
        """サインイン情報がない時のActionViewを構成する"""
        for la in self.children.copy():
            if isinstance(la, LaButton):
                self.remove_widget(la)
        self.action_previous.funcname = "menu"
        self.add_widget(LaButton(text="Sign in"))
        self.add_widget(LaButton(text="Sign up"))

    def signed(self):
        """サインイン情報がある時のActionViewを構成する"""
        for la in self.children.copy():
            if isinstance(la, LaButton):
                self.remove_widget(la)
        self.action_previous.funcname = "gtl"
        self.add_widget(LaButton(text="My Page"))


class LaPrevious(ActionPrevious):
    """
    ActionView内に置く戻るボタンのWidget。
    """
    def __init__(self, fname, **kwargs):
        super(LaPrevious, self).__init__(**kwargs)
        self.funcname = fname.replace(" ", "_")

    def on_release(self):
        getattr(self, self.funcname)()

    def menu(self):
        """menuscreenに移動する。"""
        sm = App.get_running_app().root.ids["smanager"]
        sm.transition.direction = "right"
        sm.current = "menuscreen"

    def gtl(self):
        """global timelineに移動する。"""
        sm = App.get_running_app().root.ids["smanager"]
        sm.gtl()


class LaButton(ActionButton):
    """
    LaButton: ActionView内に置くボタンのWidget。
    """
    def __init__(self, **kwargs):
        super(LaButton, self).__init__(**kwargs)
        funcname = kwargs["text"].replace(" ", "_")
        self.on_release = getattr(self, funcname)

    def Sign_in(self):
        """サインイン画面に移動する。"""
        sm = App.get_running_app().root.ids["smanager"]
        sm.transition.direction = "left"
        sm.current = "signinform"

    def Sign_up(self):
        """サインアップ画面に移動する。"""
        sm = App.get_running_app().root.ids["smanager"]
        sm.transition.direction = "left"
        sm.current = "signupform"

    def My_Page(self):
        """自分のユーザー画面に移動する。"""
        sm = App.get_running_app().root.ids["smanager"]
        sm.user()



kv = r"""
<LaPrevious>:
    title: "Akitter"
    color: 0.937, 0.506, 0.059, 1 #orange
    app_icon: "./images/Akitter.png"

<LaButton>:
    color: 0.937, 0.506, 0.059, 1 #orange
"""

Builder.load_string(kv)