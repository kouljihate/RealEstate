from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton

KV = """
<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        spacing: 24
        padding: [32, 48]
        md_bg_color: app.theme_cls.bg_normal

        Image:
            source: "data/logo.png" if exists else ""
            size_hint_y: 0.2
            pos_hint: {"center_x": 0.5}

        MDLabel:
            text: "RealEstate"
            font_style: "H3"
            halign: "center"
            theme_text_color: "Primary"

        MDLabel:
            text: "Farm Land Marketplace"
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Secondary"

        MDTextField:
            id: email_input
            hint_text: "Email"
            mode: "rectangle"
            icon_right: "email"
            input_filter: "email"
            required: True

        MDTextField:
            id: password_input
            hint_text: "Password"
            mode: "rectangle"
            icon_right: "lock"
            password: True
            required: True

        MDRaisedButton:
            text: "Sign In"
            size_hint_x: 1
            height: 52
            on_release: app.root.get_screen("login").do_login()

        MDLabel:
            id: error_label
            text: ""
            halign: "center"
            theme_text_color: "Error"
            size_hint_y: 0.1

        MDFlatButton:
            text: "Don't have an account?"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "register"
"""

Builder.load_string(KV)


class LoginScreen(Screen):
    def do_login(self):
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text

        if not email or not password:
            self.ids.error_label.text = "Please fill all fields"
            return

        try:
            app = MDApp.get_running_app()
            app.api.login(email, password)
            user = app.api.get_me()
            app.login_success(user)
        except Exception as e:
            self.ids.error_label.text = str(e)


from kivymd.app import MDApp
