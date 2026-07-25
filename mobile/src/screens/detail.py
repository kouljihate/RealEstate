from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

KV = """
<DetailScreen>:
    name: "detail"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Property Details"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'properties')]]

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: [16, 16]
                spacing: 12
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    id: prop_title
                    font_style: "H5"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    id: prop_price
                    font_style: "H4"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    id: prop_location
                    font_style: "Subtitle1"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDSeparator:

                MDLabel:
                    id: prop_description
                    size_hint_y: None
                    height: self.texture_size[1]

                MDSeparator:

                MDLabel:
                    id: prop_features
                    size_hint_y: None
                    height: self.texture_size[1]

                MDRaisedButton:
                    text: "Contact Seller"
                    size_hint_x: 1
                    height: 52
"""

Builder.load_string(KV)


class DetailScreen(Screen):
    property_id = None

    def on_enter(self):
        if self.property_id:
            self.load_detail()

    def load_detail(self):
        app = MDApp.get_running_app()
        try:
            prop = app.api.get_property(self.property_id)
            self.ids.prop_title.text = prop.get("title", "")
            self.ids.prop_price.text = f"${prop.get('price', 0):,}"
            loc = prop.get("location", {})
            self.ids.prop_location.text = f"{loc.get('address', '')}, {loc.get('city', '')}, {loc.get('state', '')}"
            self.ids.prop_description.text = prop.get("description", "")
            features = prop.get("features", [])
            self.ids.prop_features.text = "Features:\n" + "\n".join(f"• {f}" for f in features) if features else ""
        except Exception as e:
            from kivymd.uix.dialog import MDDialog
            MDDialog(text=f"Error: {e}").open()
