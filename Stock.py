import twstock as stock

class Get:
    def stock(self, code):
        search = stock.Stock(code)
        open_price = search.open[-1]
        close_price = search.close[-1]
        high_price = search.high[-1] 
        low_price = search.low[-1]
        return {'open': open_price, 'close': close_price, 'high': high_price, 'low': low_price}