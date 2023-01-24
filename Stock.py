import pandas as pd
import yfinance as yf
import twstock as stock
import matplotlib.pyplot as plt

code = input('輸入股票代碼：')

if code.isdigit():
    try:
        search = stock.Stock(code)
        open = search.open[-1:]
        close = search.close[-1:]
        high = search.high[-1:] 
        low = search.low[-1:]
        delstring = str.maketrans({'[':'',']':''})
        print(f'開盤價：{open}'.translate(delstring))
        print(f'收盤價：{close}'.translate(delstring))
        print(f'最高價：{high}'.translate(delstring))
        print(f'最低價：{low}'.translate(delstring))
        start = input('輸入開始日期(格式：西元年份-月-日)：')
        end = input('輸入結束日期(格式：西元年份-月-日)：')
        history = yf.download(code + '.TW', start=start, end=end)
        print(history)
        plt.style.use('ggplot')
        history['Adj Close'].plot(figsize=(10,6))
        chart = pd.DataFrame(history['Adj Close']).reset_index().rename(columns={'Date':'ds', 'Adj Close':'y'}) # 建立時間(ds)對應的收盤價(y)數據
        chart.head()
        plt.show()
    except KeyError:
        print('股票代碼輸入有誤！')
        
if code.isalpha():
    start = input('輸入開始日期(格式：西元年份-月-日)：')
    end = input('輸入結束日期(格式：西元年份-月-日)：')
    history = yf.download(code, start=start, end=end)
    print(history)
    plt.style.use('ggplot')
    history['Adj Close'].plot(figsize=(10,6))
    chart = pd.DataFrame(history['Adj Close']).reset_index().rename(columns={'Date':'ds', 'Adj Close':'y'})
    chart.head()
    plt.show()