from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup



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
        """poperror: エラーメッセージを出す。"""
        self.popup = ErrorPopup(text=text)
        self.popup.open()



kv = r"""
<ErrorPopup>:
    title: "error"
    size_hint: None, None
    size: sp(300), sp(300)

    BoxLayout:
        orientation: "vertical"

        Label:
            text: root.text

        Button:
            text: "quit"
            on_release: root.dismiss()
            size_hint_y: 0.3
"""

Builder.load_string(kv)
