import re
import os
import csv
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

class Get:
    def __init__(self):
        self.stock_id = None
        self.stock_name = None
        self.stock_type = None

    def search(self, code):
        try:
            with open('csv/twse.csv', 'r') as twse:
                reader = csv.reader(twse)
                for row in reader:
                    if len(row) >= 2:
                        if code == row[0] or code == row[1]:
                            self.stock_id = row[0] + '.TW'
                            self.stock_name = row[1]
                            self.stock_type = row[5]
                            print('上櫃公司股票代碼：' + row[0] + ' 上市公司股票名稱：' + row[1] + ' 公司類型：' + row[5])
                            return {'stock_id': self.stock_id, 'name': self.stock_name,'type': self.stock_type}
            with open('csv/tpex.csv', 'r') as tpex:
                reader = csv.reader(tpex)
                for row in reader:
                    if len(row) >= 2:
                        if code == row[0] or code == row[1]:
                            self.stock_id = row[0] + '.TWO'
                            self.stock_name = row[1]
                            self.stock_type = row[5]
                            print('上櫃公司股票代碼：' + row[0] + ' 上櫃公司股票名稱：' + row[1] + ' 公司類型：' + row[5])
                            return {'stock_id': self.stock_id, 'name': self.stock_name, 'type': self.stock_type}
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

        # First columns
        mapping = {
            0: '年度',
            1: '股本(億)',
            2: '財報評分',
            3: '收盤',
            4: '平均',
            5: '漲跌',
            6: '漲跌(%)',
            7: '營業收入',
            8: '營業毛利',
            9: '營業利益',
            10: '業外損益',
            11: '稅後淨利',
            12: '營業毛利(%)',
            13: '營業利益(%)',
            14: '業外損益(%)', 
            15: '稅後淨利(%)',
            16: 'ROE(%)',
            17: 'ROA(%)',
            18: '稅後EPS',
            19: '年增(元)',
            20: 'BPS(元)'
            }
            
        labels = [mapping.get(col) for col in columns]
        df.columns = labels

        return df

    def find_col(self, code, args, rows):
        df = pd.read_csv(f'finance/{code}.csv')
        select_cols = df[list(args)].head(rows) # Find the specified columns
        result = [' '.join(args)] + select_cols.to_string(index = False).split('\n')[1:]
        # [' '.join(args)] Header and header spaces
        # [1:] Avoid 2 headers (ex:年度 ...', '2022 ...' to '2022 ...')
        return '\n'.join(result)

    def goodinfo_to_csv(self, code, *args, rows: int):
        code = re.sub(r'\.(TW|TWO)$', '', code)
        file_path = f'finance/{code}.csv'

        if os.path.isfile(file_path):
            return self.find_col(code, args, rows)

        else:
            url = f'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={code}'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
            res = requests.get(url, headers = headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('div', {'id': 'txtFinDetailData'}).find('table')

            df = pd.read_html(str(table), header = None, skiprows = 1)[0]
            df = df[~df.astype(str).apply(lambda row: row.str.contains('[\u4e00-\u9fff]').any(), axis=1)]
            df.columns = df.columns.map(lambda x: x[0].replace(' ', '') if isinstance(x, tuple) else x.replace(' ', '')) # Remove spaces in column headers

            # Add (%) to the second header
            col_counts = df.columns.value_counts()
            duplicated_col = col_counts[col_counts > 1].index # Find duplicate columns (ex: Index(['營業毛利', '...'], dtype='object'))

            for columns in duplicated_col:
                duplicated_indices = [i for i, col in enumerate(df.columns) if col == columns] # Find the indices of duplicate columns (ex: [8, 12])
                for index in duplicated_indices[1:]:
                    df.columns.values[index] += '(%)'

            df.to_csv(f'finance/{code}.csv', index = False)
            print(f'{code}.csv 財報檔案已創建！')

            return self.find_col(code, args, rows)