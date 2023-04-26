
from ast import expr_context
import re
from tracemalloc import stop
import requests
import yfinance as yf
from bs4 import BeautifulSoup

class Get:
    def search(self, code):
        if all('\u4e00' <= char <= '\u9fff' for char in code) or code.isdigit():
            url = f'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={code}'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            if '您的瀏覽量異常, 已影響網站速度, 目前暫時關閉服務' in html:
                error = '暫時無法讀取資料'
                return {'stock_id': error}
            else:
                for link in soup.find_all('a', class_='link_blue'):
                    if re.search('StockDetail\.asp\?STOCK_ID=(\d+)', link.get('href')):
                        stock_id = re.search('STOCK_ID=(\d+)', link.get('href')).group(1)
                        return {'stock_id': stock_id + '.TW'}

        if code.isalpha():
            self.price(code)
            return {'stock_id': code}

    def price(self, code):
        data = yf.download(code , period = '1d', rounding = True)
        open = str(data.iloc[0]['Open'])
        close = str(data.iloc[0]['Close'])
        high = str(data.iloc[0]['High'])
        low = str(data.iloc[0]['Low'])
        return {'open': open, 'close': close, 'high': high, 'low': low}

    def financial(self, code):
        try:
            data = yf.Ticker(code)
            pe = data.info['trailingPE']
            pe_rounded = '{:.2f}'.format(pe)
            return {'pe': pe_rounded}
        except KeyError:
            return {'pe': '查無本益比資訊'}