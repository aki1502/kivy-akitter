from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView

import modules.multi_language_textinput

from modules.akeet import Akeet
from modules.errorpopper import ErrorPopper
import modules.separator



initial_string = "You can use only 31 characters."

class AkeetForm(ErrorPopper):
    """
    AkeetForm: TL+Akeet投稿画面のWidget。
    """
    ipt = StringProperty()

    def __init__(self, **kwargs):
        super(AkeetForm, self).__init__(**kwargs)
        self.ipt = initial_string

    def send(self):
        """send: Akeetを投稿する。"""
        self.ipt = self.ids["textinput"].text
        if self.ipt == "":
            return None
        error_message = self.invalid(self.ipt)
        if error_message:
            self.poperror(error_message)
        else:
            print(self.ipt)
            self.ipt = ""

    def invalid(self, text):
        """invalid: Akeetが不適か調べる。返り値は文字列。"""
        l = len(text)
        if "\n" in text:
            return "改行文字は使えません。"
        if l > 31:
            return "三十一文字しか使えません。"
        if initial_string[:l] == text:
            return "予め入っている文は投稿できません。"
        return ""

    def user_detail(self, name):
        """user_detail: ユーザー詳細画面に遷移する。"""
        self.manager.user(name)


class AkeetColumn(RecycleView):
    """
    AkeetColumn: TLのWidget。
    """
    def __init__(self, **kwargs):
        super(AkeetColumn, self).__init__(**kwargs)
        self.data = [Akeet().row() for i in range(100)]



formkv = r"""
<AkeetForm>:
    textinput_font_size: self.width/sp(35) if self.width > 14*sp(37) else self.width/sp(23)
    textinput_height: self.width/sp(26)+sp(10) if self.width > 14*sp(37) else self.width/sp(8)+sp(5)
    sendbutton_width: self.width/sp(12) if self.width > 14*sp(37) else self.width/sp(8)
    orientation: "vertical"

    AkeetColumn:
        viewclass: "AkeetRow"
        scroll_y: 0

        size_hint_y: None
        height: root.height-root.textinput_height
        pos: (0, root.textinput_height)
        padding: 0, sp(2), 0, 0

        RecycleBoxLayout:
            default_size: None, root.width/10 if self.width > 14*sp(37) else self.width/6
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: root.textinput_height

        FloatLayout:
            size_hint_x: None
            width: root.width-root.sendbutton_width

            TextInputIME:
                id: textinput
                font_size: root.textinput_font_size
                composition_window: cmp_window
                text: root.ipt
                multiline: True
                on_touch_up: self.select_all()
                cursor_blink: True
                cursor_color: 0.937, 0.506, 0.059, 0.8 # orange
                selection_color: 0.937, 0.506, 0.059, 0.221 # orange
                pos: (sp(2), 0)

            CompositionLabel:
                id: cmp_window
                font_size: root.textinput_font_size
                textinput: textinput
                x: textinput.cursor_pos[0]
                y: textinput.cursor_pos[1] - self.height

        Button:
            font_size: root.textinput_font_size
            text: "send"
            color: 0.937, 0.506, 0.059, 1 #orange
            size_hint_x: None
            width: root.sendbutton_width
            on_release: root.send()
"""

akeetkv = r"""
<AkeetRow@BoxLayout>:
    color: 0.941, 0.973, 1, 1 #aliceblue
    icon: "./images/anonymous.png"
    author: "aki1502"
    text: "こんにちは、世界！"
    date: "1998/02/21 20:00"
    font_size: self.width/sp(37) if self.width > 14*sp(37) else self.width/sp(24)

    orientation: "vertical"

    canvas.before:
        Color:
            rgba: 0.439, 0.502, 0.565, 1 #slategray
        Rectangle:
            pos: self.pos
            size: self.size

    Separator:

    BoxLayout:
        orientation: "horizontal"

        AnchorLayout:
            anchor_x: "left"
            anchor_y: "top"
            size_hint_x: None
            width: root.font_size*3+sp(20)

            Image:
                height: root.font_size*3
                source: root.icon

        BoxLayout:
            orientation: "vertical"

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 1 if root.width > 14*sp(37) else 0.5

                Label:
                    markup: True
                    text: "[ref=author]"+root.author+"[/ref]"
                    on_ref_press: app.root.ids.akeetform.user_detail(root.author)
                    color: 0.937, 0.506, 0.059, 1 #orange
                    font_size: root.font_size
                    text_size: self.size
                    halign: "left"
                    valign: "center"

                Label:
                    text: root.date
                    color: 0.8, 0.8, 0.9, 1
                    font_size: root.font_size
                    text_size: self.size
                    halign: "right"
                    valign: "center"
                    padding_x: sp(10)

            Label:
                text: root.text
                font_size: root.font_size
                text_size: self.size
                halign: "left"
                valign: "top"
"""

Builder.load_string(formkv)
Builder.load_string(akeetkv)