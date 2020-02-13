from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
import requests

from modules.akeet import Akeet
from modules.errorpopper import ErrorPopper
import modules.multi_language_textinput
import modules.separator
from data.loginfo import getloginfo
from variables import config, url



initial_string = "You can use only 31 characters."

class AkeetForm(ErrorPopper):
    """
    TL+Akeet投稿画面のWidget。
    """
    ipt = StringProperty()

    def __init__(self, **kwargs):
        super(AkeetForm, self).__init__(**kwargs)
        self.ipt = initial_string

    def send(self):
        """Akeetを投稿する。"""
        self.ipt = self.ids["textinput"].text
        if self.ipt == "":
            return None
        error_message = self.invalid(self.ipt)
        if error_message:
            self.poperror(error_message)
            return None
        r = requests.post(
            url.AKEETS,
            json={"text": self.ipt},
            headers={"Authorization": f"Token {getloginfo()['auth_token']}"}
        )
        if r.status_code == 201:
            self.ipt = ""
        elif r.status_code == 401:
            self.poperror("ログイン情報が見つかりません。")
        else:
            self.poperror(r.json()["detail"])

    def invalid(self, text):
        """Akeetが不適か調べる。返り値は文字列。"""
        l = len(text)
        if "\n" in text:
            return "改行文字は使えません。"
        if l > 31:
            return "三十一文字しか使えません。"
        if initial_string[:l] == text:
            return "予め入っている文は投稿できません。"
        return ""


class AkeetColumn(RecycleView):
    """
    TLのWidget。
    """
    def __init__(self, **kwargs):
        super(AkeetColumn, self).__init__(**kwargs)
        self.end = datetime(1998, 2, 21)
        self.data = self.get_akeets()
        executor = ThreadPoolExecutor()
        executor.daemon = True
        executor.submit(self.daemon)

    def get_akeets(self):
        """最新のAkeetを取得する。"""
        start, self.end = self.end, datetime.now()
        r = requests.get(
            url.AKEETS,
            {
                "published_date_after": start.isoformat(sep=" "),
                "published_date_before": self.end.isoformat(sep=" ")
            }
        )
        data = reversed(r.json())
        return deque((Akeet.from_response(r).row() for r in data), 100)

    def daemon(self):
        """新規Akeetを取得し続ける。(config.qt==Falseの間)"""
        config.qt = False
        while not config.qt:
            sleep(1)
            self.data.extend(self.get_akeets())



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
            padding_x: sp(2)
"""

akeetkv = r"""
<AkeetRow@BoxLayout>:
    color: 0.941, 0.973, 1, 1 #aliceblue
    icon: "./images/anonymous.png"
    author: "aki1502"
    text: "こんにちは、世界！"
    published_date: "1998/02/21 20:00"
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
            width: root.height+sp(4)

            Image:
                height: root.height
                source: root.icon

        BoxLayout:
            orientation: "vertical"

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 1 if root.width > 14*sp(37) else 0.5

                Label:
                    markup: True
                    text: "[ref=author]"+root.author+"[/ref]"
                    on_ref_press: app.root.ids.smanager.user(name=root.author)
                    color: 0.937, 0.506, 0.059, 1 #orange
                    font_size: root.font_size
                    text_size: self.size
                    halign: "left"
                    valign: "center"
                    padding_x: sp(5)

                Label:
                    text: root.published_date
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
                padding_x: sp(5)
"""

Builder.load_string(formkv)
Builder.load_string(akeetkv)



if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(Builder.load_string(r"AkeetForm:"))