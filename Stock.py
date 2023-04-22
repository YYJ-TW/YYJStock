import twstock as stock
from twstock import BestFourPoint

class Get:
    def price(self, code):
        search = stock.Stock(code)
        open_price = search.open[-1]
        close_price = search.close[-1]
        high_price = search.high[-1] 
        low_price = search.low[-1]
        return {'open': open_price, 'close': close_price, 'high': high_price, 'low': low_price}
    
    def best(self, code):
        search = stock.Stock(code)
        bfp = BestFourPoint(search)
        buy = bfp.best_four_point_to_buy()
        sell = bfp.best_four_point_to_sell()
        point = bfp.best_four_point()
        return {'buy': buy, 'sell': sell, 'point': point}
