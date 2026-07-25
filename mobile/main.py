"""
RealEstate Mobile App - KivyMD Android Application
Entry point for the mobile farm land marketplace app.
"""

from kivy.config import Config

Config.set("kivy", "window_icon", "icon.png")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "700")

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uiz_card import MDCardSwipe

from mobile.src.services.api import ApiService
from mobile.src.screens.login import LoginScreen
from mobile.src.screens.home import HomeScreen
from mobile.src.screens.properties import PropertiesScreen
from mobile.src.screens.detail import DetailScreen

KV = """
MDScreenManager:
    LoginScreen:
    HomeScreen:
    PropertiesScreen:
    DetailScreen:
"""


class RealEstateApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = ApiService()
        self.current_user = None
        self.sm = ScreenManager()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        self.sm = Builder.load_string(KV)
        self.sm.current = "home"
        return self.sm

    def on_start(self):
        token = self.api.get_saved_token()
        if token:
            try:
                self.api.set_token(token)
                self.current_user = self.api.get_me()
                if self.current_user:
                    self.sm.current = "home"
                    return
            except Exception:
                self.api.set_token(None)
        self.sm.current = "login"

    def login_success(self, user):
        self.current_user = user
        self.sm.current = "home"

    def logout(self):
        self.api.set_token(None)
        self.current_user = None
        self.sm.current = "login"


if __name__ == "__main__":
    RealEstateApp().run()
