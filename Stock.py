import re
import csv
import datetime
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

class Get:
    def __init__(self):
        self.stock_id = None
        self.stock_type = None

    def search(self, code):
        try:
            with open('csv/twse.csv', 'r') as twse:
                reader = csv.reader(twse)
                for row in reader:
                    if len(row) >= 2:
                        if code == row[0] or code == row[1]:
                            self.stock_id = row[0] + '.TW'
                            self.stock_type = row[5]
                            print('上市公司股票編號' + row[0] + ' 公司類型：' + row[5])
                            return {'stock_id': self.stock_id, 'type': self.stock_type}
            with open('csv/tpex.csv', 'r') as tpex:
                reader = csv.reader(tpex)
                for row in reader:
                    if len(row) >= 2:
                        if code == row[0] or code == row[1]:
                            self.stock_id = row[0] + '.TWO'
                            self.stock_type = row[5]
                            print('上櫃公司股票編號：' + row[0] + ' 公司類型：' + row[5])
                            return {'stock_id': self.stock_id, 'type': self.stock_type}
            return None
            
        except:
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
           

    def price(self, code):
        data = yf.download(code , period = '1d', rounding = True)
        open = str(data.iloc[0]['Open'])
        close = str(data.iloc[0]['Close'])
        high = str(data.iloc[0]['High'])
        low = str(data.iloc[0]['Low'])
        return {'open': open, 'close': close, 'high': high, 'low': low}

    def yf_fin(self, code):
        try:
            data = yf.Ticker(code)
            pe = data.info['trailingPE']
            pe_rounded = '{:.2f}'.format(pe)
            eps = data.info['bookValue']
            return {
                'pe': str(pe_rounded),
                'bv': str(eps),   
            }
        except KeyError as e:
            print(e)
            return {
                'pe': '查無本益比資訊',
                'bv': '查無EPS資訊',
            }
    
    def goodinfo_fin(self, code, columns, years):
        code = re.sub(r'\.(TW|TWO)$', '', code)
        url = f'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={code}'
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find('div', {'id': 'txtFinDetailData'}).find('table')
        rows = table.find_all('tr')

        data = []
        count = 0

        for row in rows:
            tds = row.find_all('td')
            if len(tds) > 1: # Avoid None
                values = []
                for col in columns:
                    if col < len(tds):
                        value = tds[col].text.strip()
                        if not re.search('[\u4e00-\u9fff]', value):
                            values.append(value)
                data.append(values)
                count += 1
                if count >= years:
                    break

        df = pd.DataFrame(data, columns = values)
        return df