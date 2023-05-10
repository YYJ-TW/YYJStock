# Class
from stock import Get
# Data
import pandas as pd

class Analyze:
    def basic_fin(self, df):
        values = df.iloc[0:2, 1].values

        if values[0] > values[1]:
            judge = '成長'
        elif values[0] < values[1]:
            judge = '下跌'

        return judge