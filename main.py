from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


store = JsonStore('data.json')


class CustomBtn(Button):
    key_name = StringProperty()


class Interface(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.fetching_data)

    def truncate_string(self, input_str: str, max_length: int):

        if len(input_str) > max_length:
            return input_str[:max_length - 3].strip() + '...'

        return input_str

    def deleting(self, obj):
        id = obj.key_name
        self.ids.gridlayout.remove_widget(self.ids[id])
        store.delete(id)

    def fetching_data(self, dt):
        try:
            keys = store.keys()

            for key in keys:
                layout = BoxLayout(
                    spacing=dp(10),
                    size_hint=(0.7, None),
                    height=dp(60)
                )
                self.ids[key] = layout

                title = CustomBtn(
                    background_normal='orange-gradient.png',
                    key_name=key,
                    text=self.truncate_string(key, 15),
                    font_size='18sp',
                    font_name='keaniaone-regular.ttf'
                )
                title.bind(on_press=self.detail_screen)

                delete = CustomBtn(
                    background_normal='delete_icon.png',
                    key_name=key,
                    text='',
                    size_hint=(None, None),
                    size=(dp(60), dp(60))
                )
                delete.bind(on_press=self.deleting)

                layout.add_widget(title)
                layout.add_widget(delete)

                self.ids.gridlayout.add_widget(layout)
        except:
            print('store is empty')

    def back(self):

        store.put(self.ids.notice_titles.text, data=self.ids.input_data.text)

        self.transition.direction = 'right'
        self.current = 'Main Screen'

    def detail_screen(self, obj):
        self.transition.direction = 'left'

        self.ids.notice_titles.text = obj.key_name
        self.ids.notice_titles.font_size = '24sp'
        self.ids.input_data.text = store.get(obj.key_name)['data']

        self.current = 'Details Screen'


    def add_item(self, obj):
        self.popup.dismiss()
        layout = BoxLayout(
            spacing=dp(10),
            size_hint=(0.7, None),
            height = dp(60)
        )
        title = CustomBtn(
            background_normal='orange-gradient.png',
            key_name=self.text_input.text,
            text=self.truncate_string(self.text_input.text, 15),
            font_size='18sp',
            font_name='keaniaone-regular.ttf'
        )
        title.bind(on_press=self.detail_screen)

        delete = CustomBtn(
            background_normal='delete_icon.png',
            key_name=self.text_input.text,
            text='',
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )
        delete.bind(on_press=self.deleting)
        self.ids[self.text_input.text] = layout

        layout.add_widget(title)
        layout.add_widget(delete)

        store.put(self.text_input.text, data='')

        self.ids.gridlayout.add_widget(layout)

    def show_popup(self):
        layout = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))

        btn = Button(
            background_normal='',
            background_color=(0.329, 0.157, 0.647, 1),
            text='Submit',
            font_name='keaniaone-regular.ttf'
        )
        btn.bind(on_press=self.add_item)
        self.text_input = TextInput(multiline=False, font_name='keaniaone-regular.ttf')
        self.text_input.bind(on_text_validate=self.add_item)

        layout.add_widget(self.text_input)
        layout.add_widget(btn)

        self.popup = Popup(
            title='Notice Title',
            title_font='keaniaone-regular.ttf',
            size_hint=(0.9, None),
            height=dp(180),
            content=layout
        )
        self.popup.open()


class ToDoApp(App):
    pass


if __name__ == '__main__':
    ToDoApp().run()
