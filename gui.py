# Class
from stock import Get
from chart import generate_chart
# GUI
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel

kv = '''
<TextInput>:
    font_name: 'fonts/jf-openhuninn-2.0.ttf'
    
<Label>:
    font_name: 'fonts/jf-openhuninn-2.0.ttf'
'''

Builder.load_string(kv)
Builder.load_file('kivy.kv')

class MyLayout(TabbedPanel):
    pass

class YYJStock(App):
    def build(self):
        return MyLayout()

    def on_enter(self, instance):
        code = instance.text
        search = Get().search(code)
        stock_id = search.get('stock_id')
        price = Get().price(stock_id)
        financial = Get().financial(stock_id)
        self.root.ids.label.text = '股票代碼：' + stock_id + '\n開盤：' + price['open'] + '\n收盤：' + price['close'] + '\n最高：' + price['high'] + '\n最低：' + price['low']
        self.root.ids.financial.text = str('目前本益比：' + financial['pe'])
        try:
            generate_chart(search.get('stock_id'))
            self.root.ids.img.source = 'chart.png'
            self.root.ids.img.reload()
        except:
            self.root.ids.img.source = 'oops.png'
            self.root.ids.img.reload()

if __name__ == '__main__':
    YYJStock().run()