from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.card import MDCardSwipe

KV = """
<PropertiesScreen>:
    name: "properties"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Properties"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'home')]]

        ScrollView:
            MDList:
                id: property_list
                spacing: 8
                padding: [8, 8]
"""

Builder.load_string(KV)


class PropertiesScreen(Screen):
    def on_enter(self):
        self.load_properties()

    def load_properties(self):
        app = MDApp.get_running_app()
        self.ids.property_list.clear_widgets()

        try:
            data = app.api.get_properties()
            items = data.get("items", [])
            for prop in items:
                item = ThreeLineListItem(
                    text=prop.get("title", ""),
                    secondary_text=f"${prop.get('price', 0):,} | {prop.get('area_hectares', 0)} ha",
                    tertiary_text=f"{prop.get('location', {}).get('city', '')}, {prop.get('location', {}).get('state', '')}",
                    on_release=lambda p=prop: self.open_detail(p.get("id")),
                )
                self.ids.property_list.add_widget(item)
        except Exception as e:
            from kivymd.uix.dialog import MDDialog
            MDDialog(text=f"Error loading properties: {e}").open()

    def open_detail(self, property_id):
        screen = app.root.get_screen("detail")
        screen.property_id = property_id
        app.root.current = "detail"
