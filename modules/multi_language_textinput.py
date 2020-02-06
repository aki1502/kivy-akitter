import ctypes
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.utils import platform
from kivy.base import EventLoop
from kivy.properties import (
    StringProperty, ObjectProperty, NumericProperty, ListProperty
    )
from kivy.lang import Builder
from kivy.utils import escape_markup


def sets(family, *filenames):
    for f in filenames:
        try:
            LabelBase.register(family, f)
            break
        except BaseException:
            pass


if platform == 'win':

    resource_add_path('c:/Windows/Fonts')
    sets(DEFAULT_FONT, 'YuGothR.ttc')

    dll = ctypes.cdll.LoadLibrary('./modules/ime_operator.dll')

    dll.getCandidate.restype = ctypes.c_char_p
    dll.getComposition.restype = ctypes.c_char_p
    dll.getEnterdString.restype = ctypes.c_char_p  # POINTER(ctypes.c_char)

else:
    class Dummy:
        def getCandidate(self, *args):
            return b''

        def getComposition(self, *args):
            return b''

        def getEnterdString(self, *args):
            return b''

        def getIsOpenIME(self, *args):
            return 0

        def getEnteredString(self, *args):
            return b''

    dll = Dummy()


class TextInputIME(TextInput):

    composition_string = StringProperty()
    sdl_composition = StringProperty()
    composition_window = ObjectProperty()
    candidate_window = ObjectProperty()
    old_cursor_color = ListProperty()
    composition_cursor_index = NumericProperty()

    def __init__(self, **kwargs):

        super(TextInputIME, self).__init__(**kwargs)

        self.disable_on_textedit = (False, False)
        self.is_openIME = False
        self.old_cursor_color = self.cursor_color
        self.old_composition = ''

        EventLoop.window.bind(on_textedit=self._on_textedit)

    def _on_textedit(self, _, value):
        '''
        when there is nothing to be acquired,
        'getEnterdSting','getComposition','getCandidate'
        function returns '\n\n'.
        (It's because I think that IME will not returns '\n\n')

        valiable of value can only retains
        about 15 charactors.

        But 'on_textedit' event is fired when size of composition
        string exceeds 15 too.

        So when fired the event,this function does
        processing such as acquistion candidates.

        返すべき値がないとき、
        'getEnterdSting','getComposition','getCandidate'
        これらの関数は、'\n\n'という文字列を返します。（IMEからこの文字列が
        取得されることがあるとは考えられないからです）

        なおSDL2の制約により、この関数の引数であるvalueには15文字程度以上
        は保持出来ません。しかし、texteditイベント自体は入力中の文字が15文字
        を超えても発火されるため、このイベントが呼ばれたタイミングで
        変換候補取得などの処理をしています。
        '''
        self.sdl_composition = value
        self.is_openIME = bool(dll.getIsOpenIME())

        try:
            entered_text = dll.getEnterdString().decode('cp932')
            composition_string = dll.getComposition().decode('cp932')
            candidates = dll.getCandidate().decode('cp932').split()
        except UnicodeError:
            print('failed to decode IME information')

        escaped_text = '\n'.join(
            [f'[ref={escape_markup(i)}]' + escape_markup(i) + '[/ref]'
             for i in candidates]
             )

        if composition_string != '\n\n':
            self.composition_string = composition_string
        else:
            self.composition_string = ''

        if (entered_text != '\n\n' and self.is_openIME and
                self.old_composition != value):
            index = self.cursor_index()
            self.text = self.text[:index - 1] + \
                entered_text + self.text[index:]
            self.composition_string = ''
            self.old_composition = value
            return None

        self.old_composition = value

    def insert_text(self, substring, from_undo=False):

        if substring == self.sdl_composition:
            return None
        else:
            return super(TextInputIME, self).insert_text(substring, from_undo)

    def keyboard_on_key_down(self, window, keycode, text, modifiers, dt=0):

        cursor_operations = {'left', 'up', 'right', 'down', 'backspace', 'tab'}
        self.composition_cursor_index = len(self.composition_string)

        if keycode[1] == 'left':
            self.composition_cursor_index -= 1

        if keycode[1] == 'right':
            self.composition_cursor_index += 1

        if keycode[1] in cursor_operations and self.composition_string:
            return None

        return super(
            TextInputIME,
            self).keyboard_on_key_down(
            window,
            keycode,
            text,
            modifiers)

    def on_composition_string(self, _, value):

        if self.composition_string:
            self.cursor_color = (0, 0, 0, 0)
        else:
            self.cursor_color = self.old_cursor_color

        if not dll.getIsOpenIME():
            return

        # this is to underline text.
        # 下線を引くための処理です。
        # https://kivy.org/doc/stable/api-kivy.core.text.markup.html
        self.composition_window.text = '[u]' + value + '[/u]'

    def select_candidate(self, text):

        self.focus = True
        self.readonly = False
        text = text.encode('cp932')
        text = ctypes.create_string_buffer(text)
        dll.setComposition(text)


class CompositionLabel(Label):
    textinput = ObjectProperty()