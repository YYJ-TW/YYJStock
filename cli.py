import argparse
from stock import Get

parser = argparse.ArgumentParser()
parser.add_argument('code', help = '台灣股票代碼')
parser.add_argument('columns', type = int, help = '搜尋第幾列的資料')
parser.add_argument('years', type = int, help = '搜尋多少年度的資料')

args = parser.parse_args()

result = Get().goodinfo_fin(args.code, args.columns, args.years)
print(result)
