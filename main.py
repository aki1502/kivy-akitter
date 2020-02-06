from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
import japanize_kivy
from modules.multi_language_textinput import *

initial_string = "You can use only 31 characters."


class AkitterApp(App):
    """main app for Akitter"""

    def build(self):
        return AkitterRoot()
        

class AkitterRoot(Widget):
    """root widget for Akitter"""
    
    def author_name(self, name):
        print(name)

    
class AkeetForm(BoxLayout):
    ipt = StringProperty()
    opt = StringProperty()

    def __init__(self, **kwargs):
        super(AkeetForm, self).__init__(**kwargs)
        self.ipt = initial_string
        self.opt = ""

    def send(self):
        self.ipt = self.ids["textinput"].text
        if valid(self.ipt):
            self.ipt, self.opt = "", self.ipt
        else:
            self.poperror("invalid text")

    def poperror(self, txt):
        pass



class AkeetColumn(RecycleView):
    def __init__(self, **kwargs):
        super(AkeetColumn, self).__init__(**kwargs)
        self.data = [{"icon": "./images/Akitter.png", "text": "こんにちは、世界！"} for i in range(32, 100)]


def valid(text):
    l = len(text)
    if "\n" in text:
        return False
    if l > 31:
        return False
    if initial_string[:l] == text:
        return False
    return True


if __name__ == "__main__":
    app = AkitterApp()
    app.run()