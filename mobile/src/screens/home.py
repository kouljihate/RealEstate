from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.card import MDCard

KV = """
<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "RealEstate"
            left_action_items: [["menu", lambda x: None]]
            right_action_items: [["logout", lambda x: app.logout()]]

        ScrollView:
            MDGridLayout:
                cols: 1
                spacing: 12
                padding: [16, 16]
                adaptive_height: True

                MDLabel:
                    text: "Welcome to RealEstate"
                    font_style: "H4"
                    halign: "center"
                    size_hint_y: 0.15

                MDLabel:
                    text: "Find your perfect farm land"
                    font_style: "Subtitle1"
                    halign: "center"
                    theme_text_color: "Secondary"
                    size_hint_y: 0.1

                MDRaisedButton:
                    text: "Browse Properties"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5}
                    height: 52
                    on_release: app.root.current = "properties"

                MDRaisedButton:
                    text: "List Your Land"
                    size_hint_x: 0.8
                    pos_hint: {"center_x": 0.5}
                    height: 52
                    md_bg_color: app.theme_cls.accent_color
                    on_release: app.root.current = "create_property"
"""

Builder.load_string(KV)


class HomeScreen(Screen):
    pass
