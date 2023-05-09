# YYJStock
## 簡介
使用 Python 開發的台灣股市查詢分析軟體，投資股票需要花費許多時間研究，從選股到進場和出場，在這過程中，你可能會有個困擾，那就是每個網站的資訊都不齊全，財務報表、技術分析、公司新聞十分零散。YYJStock 將股票的重要資訊整合，並且自動化分析，讓投資股票省時簡單！
## 來源
[kivy](https://github.com/kivy/kivy) GUI 模組  
[yfinance](https://github.com/ranaroussi/yfinance) 查詢股價  
[mplfinance](https://github.com/matplotlib/mplfinance) 生成K線和交易量圖表    
[goodinfo](https://goodinfo.tw) 財報資訊  
[justfont](https://github.com/justfont/open-huninn-font) 字型使用「jf open 粉圓」  
[flaticon](https://www.flaticon.com) 圖片素材  
## 指令
```python3 cli.py -h``` 獲得指令列表
```python3 cli.py 2330 5 10``` 搜尋股票代碼 2330 (台積電)，第 5 列的財報資料(漲跌)，取得 10 年的資料。
## 速率限制
Yahoo Finance API 每小時 2000 次 / 1 IP (約等於 每秒 2次)  
Goodinfo! 台灣股市資訊網 未知  