import pandas as pd

class Analyze():
    def get_specific_field(self, code, col, start_row, end_row):
        df = pd.read_csv(f'finance/{code}.csv')

        if col not in df.columns:
            print(f'查無 {col}！')

        selected_rows = df.loc[start_row:end_row, col].tolist()
        selected_rows = pd.to_numeric(selected_rows, errors='coerce') 
        return selected_rows

    def percentage_change(self, numbers):
        percentage_changes = []
        for i in range(1, len(numbers)):
            change = ((numbers[i-1] - numbers[i]) / numbers[i-1]) * 100
            sign = f"{'+' if change >= 0 else '-'}{abs(change):.2f}%"
            percentage_changes.append(sign)
        return percentage_changes

    def analyze_data(self, data):
        average = round(sum(data) / len(data), 2)
        changes = self.percentage_change(data)
        return average, changes