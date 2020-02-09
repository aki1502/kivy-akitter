from kivy.app import App
from kivy.lang.builder import Builder

from modules.errorpopper import ErrorPopper
import modules.form



class SignAbstract(ErrorPopper):
    """
    SignEP: SigninForm, SignupFormの親クラス。
    """
    def sign(self, *args):
        v = self.validation(*args)
        if not v:
            self.poperror("invalid username or password")
            return None
        sm = self.manager
        sm.gtl(direction="left")
        lv = self.manager.parent.ids["laview"]
        lv.sign()
        
    def validation(self, *args):
        raise NotImplementedError


class SigninForm(SignAbstract):
    """
    SigninForm: サインイン画面のWidget。
    """
    def validation(self, name, password):
        return True


class SignupForm(SignAbstract):
    """
    SignupForm: サインアップ画面のWidget。
    """
    def validation(self, name, password1, password2):
        return True


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
                on_release: root.sign(username.text, password.text)
"""

upkv = r"""
<SignupForm>:
    BoxLayout:
        orientation: "vertical"

        Form:
            id: username
            label_text: "UserName"

        Form:
            id: passwordone
            label_text: "Password"
            password: True

        Form:
            id: passwordtwo
            label_text: "Password(again)"
            password: True

        AnchorLayout:
            Button:
                size_hint: None, None
                size: sp(300), sp(80)
                text: "Sign up"
                font_size: 35
                on_release: root.sign(username.text, passwordone.text, passwordtwo.text)
"""

Builder.load_string(inkv)
Builder.load_string(upkv)