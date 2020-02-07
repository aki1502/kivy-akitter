from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
import japanize_kivy
from modules.multi_language_textinput import *



initial_string = "You can use only 31 characters."



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


class TransitionManager(ScreenManager):
    """
    TransitionManager: 画面遷移を管理するWidget。
    """
    def __init__(self, **kwargs):
        super(TransitionManager, self).__init__(**kwargs)
        self.add_widget(MenuScreen(name="menuscreen"))
        self.add_widget(SigninForm(name="signinform"))
        self.add_widget(SignupForm(name="signupform"))
        self.add_widget(AkeetForm(name="akeetform"))


class ErrorPopup(Popup):
    """
    ErrorPopup: エラーメッセージを出すWidget。
    """
    text = StringProperty()

    def __init__(self, text="undefined error"):
        super(ErrorPopup, self).__init__()
        self.text = text


class ErrorPopper(Screen):
    """
    ErrorPopper: エラーメッセージを出せるようにするWidget。
    メッセージを出したいWidgetに継承して使う。
    """
    def poperror(self, text):
        self.popup = ErrorPopup(text=text)
        self.popup.open()


class MenuScreen(Screen):
    pass


class SigninForm(ErrorPopper):
    """
    SigninForm: サインイン画面のWidget。
    """
    def signin(self, name, password):
        if self.valid(name, password):
            self.manager.transition_direction = "right"
            self.manager.current = "akeetform"

    def valid(self, name, password):
        return True


class SignupForm(ErrorPopper):
    """
    SignupForm: サインアップ画面のWidget。
    """
    def signup(self, name, password1, password2):
        if self.valid(name, password1, password2):
            self.manager.transition_direction = "right"
            self.manager.current = "akeetform"

    def valid(self, name, password1, password2):
        return True


class AkeetForm(ErrorPopper):
    """
    AkeetForm: TL+Akeet投稿画面のWidget。
    """
    ipt = StringProperty()

    def __init__(self, **kwargs):
        super(AkeetForm, self).__init__(**kwargs)
        self.ipt = initial_string

    def send(self):
        """
        send: Akeetを投稿する。
        """
        self.ipt = self.ids["textinput"].text
        if self.ipt == "":
            return None
        error_message = self.invalid(self.ipt)
        if error_message:
            self.poperror(error_message)
        else:
            print(self.ipt)
            self.ipt = ""

    def invalid(text):
        """
        invalid: Akeetが不適か調べる。
        返り値は文字列。
        """
        l = len(text)
        if "\n" in text:
            return "改行文字は使えません。"
        if l > 31:
            return "三十一文字しか使えません。"
        if initial_string[:l] == text:
            return "予め入っている文は投稿できません。"
        return ""

    def user_detail(self, name):
        print(name)


class AkeetColumn(RecycleView):
    """
    AkeetColumn: TLのWidget。
    """
    def __init__(self, **kwargs):
        super(AkeetColumn, self).__init__(**kwargs)
        self.data = [{"icon": "./images/anonymous.png", "text": "こんにちは、世界！こんにちは、世界！こんにちは、世界！こんにち"} for i in range(32, 100)]


if __name__ == "__main__":
    app = AkitterApp()
    app.run()