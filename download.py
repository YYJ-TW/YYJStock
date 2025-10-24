# Reference: https://www.finlab.tw/python：如何獲得上市上櫃股票清單/
import requests
import pandas as pd

res = requests.get('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2') #strMode=2 上市 strMode=4 上櫃
df = pd.read_html(res.text)[0] # [0] Get only one
df.columns = df.iloc[0] # Transposing the first row to columns (有價證券代號及名稱,國際證券辨識號碼(ISIN,Code),上市日,市場別,產業別,CFICode,備註)
df = df.iloc[1:] # Columns and rows are duplicated, so removed
df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1) # Delete redundant row or columns
df = df.set_index('有價證券代號及名稱')
df.to_csv('csv/twse.csv')

# Reference: https://blog.csdn.net/weixin_43692276/article/details/104660601
dir = open('csv/twse.csv')
new = ''
for line in dir:
    new = new + ','.join(line.split()) + '\n'
print(new)
file = open('csv/twse.csv', 'w')
file.write(new)
file.close()