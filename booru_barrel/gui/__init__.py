import kivy
from kivy.app import App
from kivy.lang import Builder
from booru_barrel.gui import search, download, settings
from booru_barrel.cfg import KIVY
kivy.require(KIVY)

BarrelApp = Builder.load_string('''
#<KvLang>
<Sidebar@AnchorLayout>:
    align_x: 'left'
    align_y: 'top'
    GridLayout:
        rows: 4
        cols: 1
        Button:
            size_hint_y: None
            height: 100
            text: 'seach'
        Button:
            size_hint_y: None
            height: 100
            text: 'download'
        Button:
            size_hint_y: None
            height: 100
            text: 'settings'
        Widget:

GridLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    cols: 2
    rows: 1
    Sidebar:
        size_hint_x: None
        width: 100
        # size_hint_y: None
        # height: 300
    Label:
        text: 'content'
    # GridLayout:
    #     cols: 1
    #     rows: 2
    #         Label:
    #             text: 'search bar'
    #         Label:
    #             text: 'content'
#</KvLang>
''')

class BooruBarrelApp(App):
    def build(self):
        return BarrelApp
        

