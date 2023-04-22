# Class
from stock import Get
from chart import generate_chart
# GUI
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
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
        self.input = TextInput(hint_text='輸入股票代碼', multiline=False, size_hint=(1, None), height=50)
        self.input.bind(on_text_validate=self.on_enter)
        layout.add_widget(self.input)
        self.label = Label(text='', size_hint=(1, 1))
        self.img = Image()
        layout.add_widget(self.label)
        layout.add_widget(self.img)
        return layout

    def on_enter(self, instance):
        code = instance.text
        data = Get().price(code)
        four = Get().best(code)
        text = f"開盤：{data['open']}\n收盤：{data['close']}\n最高：{data['high']}\n最低：{data['low']}\n是否為四大買點：{four['buy']}\n是否為四大賣點：{four['sell']}\n綜合判斷：{four['point']}"
        self.label.text = text
        generate_chart(code)
        self.img.source = 'chart.png'
        self.img.reload()

if __name__ == '__main__':
    MyApp().run()
