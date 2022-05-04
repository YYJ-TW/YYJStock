import twstock as stock

code = input('請輸入股票代碼: ')
try:
    search = stock.Stock(code)
    price = search.price[-1:]
    print('收盤價: ', price)
except KeyError:
    print('未知的股票代碼!')