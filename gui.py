from stock import Get
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

kv = '''
<TextInput>:
    font_name: 'fonts/jf-openhuninn-2.0.ttf'
    
<Label>:
    font_name: 'fonts/jf-openhuninn-2.0.ttf'
'''

Builder.load_string(kv)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.input = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.input.bind(on_text_validate=self.on_enter)
        layout.add_widget(self.input)
        self.label = Label(text='', size_hint=(1, 1))
        layout.add_widget(self.label)
        return layout

    def on_enter(self, instance):
        code = instance.text
        data = Get().stock(code)
        text = f"開盤：{data['open']}\n收盤：{data['close']}\n最高：{data['high']}\n最低：{data['low']}"
        self.label.text = text

if __name__ == '__main__':
    MyApp().run()
