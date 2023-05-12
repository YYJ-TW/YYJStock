class Analyze:
    def basic_fin(self, df):
        values = df.iloc[0:3, 1].values

        if values[0] == '-':    
            if values[1] > values[2]:
                judge = '成長'
            elif values[1] < values[2]:
                judge = '下跌'
            else:
                judge= '持平'
        else:
            if values[0] > values[1]:
                judge = '成長'
            elif values[0] < values[1]:
                judge = '下跌'
            else:
                judge = '持平'

        return judge