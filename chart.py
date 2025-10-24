# Data
import os
from datetime import datetime, timedelta
# Chart
import yfinance as yf
import mplfinance as mpf

class Chart():
    def generate_chart(self, code, day):
        today = datetime.today()
        end_date = today.strftime('%Y-%m-%d')
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days = day)).strftime('%Y-%m-%d')

        data = yf.download(code, start = start_date, end = end_date)
        style = mpf.make_mpf_style(base_mpf_style = 'charles', rc = {'font.size': 10})
        mpf.plot(data, type='candle', style = style, volume = True, savefig = dict(fname = 'img/chart.png', dpi = 200, bbox_inches = 'tight'))
        return os.path.abspath('img/chart.png')