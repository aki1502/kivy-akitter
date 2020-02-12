from kivy.app import App
from kivy.lang.builder import Builder
import requests

from modules.errorpopper import ErrorPopper
import modules.form
from data.loginfo import setloginfo
from variables import url



class SignAbstract(ErrorPopper):
    """
    SigninForm, SignupFormの親クラス。
    """
    def sign(self, **kwargs):
        """sign in/upを試みる。"""
        err = self.validation(**kwargs)
        if err:
            self.poperror(err)
            return None
        sm = self.manager
        sm.gtl(direction="left")
        lv = App.get_running_app().root.ids["laview"]
        lv.signed()
        
    def validation(self, **kwargs):
        raise NotImplementedError


class SigninForm(SignAbstract):
    """
    SigninForm: サインイン画面のWidget。
    """
    def validation(self, **kwargs):
        """サインインを試みて、空文字列かエラーメッセージを送出する。"""
        r = requests.post(url.SIGNIN, json=kwargs)
        if r.status_code == 200:
            setloginfo(username=kwargs["username"], **r.json())
            return ""
        else:
            return r.json()["detail"]

class SignupForm(SignAbstract):
    """
    SignupForm: サインアップ画面のWidget。
    """
    def validation(self, **kwargs):
        """サインアップを試みて、空文字列かエラーメッセージを送出する。"""
        r = requests.post(url.SIGNUP, json=kwargs)
        if r.status_code != 201:
            if r.headers["Content-Type"] == "application/json":
                return r.json()["detail"]
            return str(r.status_code)
        r = requests.post(url.SIGNIN, json=kwargs)
        setloginfo(username=kwargs["username"], **r.json())
        return ""

inkv = r"""
<SigninForm>:
    BoxLayout:
        orientation: "vertical"

        Form:
            id: username
            label_text: "UserName"

        Form:
            id: password
            label_text: "Password"
            password: True

        Widget:

        AnchorLayout:
            Button:
                size_hint: None, None
                size: sp(300), sp(80)
                text: "Sign in"
                font_size: 35
                on_release: root.sign(username=username.text, password=password.text)
"""

upkv = r"""
<SignupForm>:
    BoxLayout:
        orientation: "vertical"

        Form:
            id: username
            label_text: "UserName"

        Form:
            id: password
            label_text: "Password"
            password: True

        Form:
            id: re_password
            label_text: "Password(again)"
            password: True

        AnchorLayout:
            Button:
                size_hint: None, None
                size: sp(300), sp(80)
                text: "Sign up"
                font_size: 35
                on_release: root.sign(username=username.text, password=password.text, re_password=re_password.text)
"""

Builder.load_string(inkv)
Builder.load_string(upkv)