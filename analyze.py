class Analyze:
    def basic_fin(self, df, col):
        values = df.iloc[0:3, col].values

        if values[0] == '-':
            diff = float(values[2]) - float(values[1])
            percentage = (diff / float(values[1])) * 100

            if percentage > 0:
                judge = f'下跌 {percentage:.2f}%'
            elif percentage < 0:
                judge = f'成長 {abs(percentage):.2f}%'
            else:
                judge = '持平'
        else:
            diff = float(values[1]) - float(values[0])
            percentage = (diff / float(values[0])) * 100

            if percentage > 0:
                judge = f'下跌 {percentage:.2f}%'
            elif percentage < 0:
                judge = f'成長 {abs(percentage):.2f}%'
            else:
                judge = '持平'

        return judge
