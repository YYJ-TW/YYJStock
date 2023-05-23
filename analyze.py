import pandas as pd

class Analyze():
    def get_specific_field(self, code, cols, start_row, end_row):
        df = pd.read_csv(f'finance/{code}.csv')

        selected_data = {}

        for col in cols:
            if col not in df.columns:
                print(f'查無 {col}！')
                continue

            selected_rows = df.loc[start_row:end_row, col].tolist() # Output: ['39.2', '23.01', '19.97', '13.32', '13.54', '13.23']
            selected_rows = pd.to_numeric(selected_rows, errors='coerce') # Output: [39.2  23.01 19.97 13.32 13.54 13.23]
            # pd.to_numeric Avoid TypeError: unsupported operand type(s) for +: 'int' and 'str'
            # errors='coerce' If there are non-numeric values in the sequence, convert them to NaN
            selected_data[col] = selected_rows # Convert the numeric sequence into a dict, use the key to get specific columns

        return selected_data # Output: {'稅後EPS': array([39.2 , ..., ...]), '營業毛利(%)': array([59.6, ..., ...])}

    def percentage_change(self, numbers):
        percentage_changes = []

        for i in range(1, len(numbers)):
            change = ((numbers[i-1] - numbers[i]) / numbers[i-1]) * 100
            sign = f"{'+' if change >= 0 else '-'}{abs(change):.2f}%"
            percentage_changes.append(sign)
            
        return percentage_changes

    def analyze_data(self, data):
        analyze_results = {}

        for col, values in data.items():
            average = round(sum(values) / len(values), 2)
            changes = self.percentage_change(values)

            analyze_results[col] = {
                'average': average,
                'changes': changes
            }
        return analyze_results # Output: {'稅後EPS': {'average': 20.38, 'changes': ['+41.30%', '...']}, '營業毛利(%)': {'average': 51.53, 'changes': ['+13.42%', '...']}}