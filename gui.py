# Class
from stock import Get
from chart import Chart
from analyze import Analyze
# GUI
from kivymd.app import MDApp
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

class YYJStock(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Gray'
        return MyLayout()

    def img(self, source):
        self.root.ids.img.source = source
        self.root.ids.img.reload()

    def on_enter(self, instance):
        code = instance.text
        get = Get()
        get.search(code)
        stock_id = get.stock_id
        self.a_stock_id = get.stock_id
        stock_name = get.stock_name
        stock_type = get.stock_type
        
        if stock_id is None: # Not found
            self.img('img/not-found.png')
        else:
            search = Get().search(code)
            stock_id = search.get('stock_id')
            self.basic_info(stock_id, stock_name, stock_type)
            self.analyze(stock_id)
            Chart().generate_chart(stock_id, 60)
            self.img('img/chart.png')
            # self.img('img/no-internet.png')

    def basic_info(self, stock_id, stock_name, stock_type):
        get = Get()
        price = get.price(stock_id)
        yf_fin = get.yf_fin(stock_id)
        fin = get.goodinfo_fin(stock_id, [0, 12, 13, 14, 15], 5)
        print(fin)
            
        label_text = f'股票代碼：{stock_id}\n股票名稱：{stock_name}\n公司類型：{stock_type}\n開盤：{price["open"]}\n收盤：{price["close"]}\n最高：{price["high"]}\n最低：{price["low"]}'
        fin_text = f'目前本益比：{yf_fin["pe"]}\n每股淨值：{yf_fin["bv"]}\n基本財報：\n{fin}'

        self.root.ids.label_text.text = label_text
        self.root.ids.financial.text = fin_text

    def update(self, value):
        print(value)
        YYJStock().analyze(self.a_stock_id, int(value))
        
    def analyze(self, stock_id, years = 2):
        get = Get()
        analyze = Analyze()
        
        fin = get.goodinfo_fin(stock_id, [0, 12, 13, 14, 15], 5)
        analyze_text = f'相比去年毛利率是{analyze.basic_fin(fin, 1, years)}\n相比去年營業利益是{analyze.basic_fin(fin, 2, years)}'
        self.root.ids.analyze.text = analyze_text

if __name__ == '__main__':
    YYJStock().run()