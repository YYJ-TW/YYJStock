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
        if stock_id == '暫時無法讀取資料':
            self.root.ids.img.source = 'oops.png'
            self.root.ids.img.reload()
        else:
            get = Get()
            price = get.price(stock_id)
            yf_fin = get.yf_fin(stock_id)
            fin = get.goodinfo_fin(stock_id)
            self.root.ids.label.text = '股票代碼：' + stock_id + '\n開盤：' + price['open'] + '\n收盤：' + price['close'] + '\n最高：' + price['high'] + '\n最低：' + price['low']
            self.root.ids.financial.text = '目前本益比：' + yf_fin['pe'] + '\n每股淨值' + yf_fin['bv'] + '\n毛利率' + fin['profit']
            generate_chart(search.get('stock_id'))
            self.root.ids.img.source = 'chart.png'
            self.root.ids.img.reload()

if __name__ == '__main__':
    YYJStock().run()