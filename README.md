# YYJStock
## 簡介
使用 Python 開發的台灣股市查詢分析軟體，投資股票需要花費許多時間研究，從選股到進場和出場，在這過程中，你可能會有個困擾，那就是每個網站的資訊都不齊全，財務報表、技術分析、公司新聞十分零散。YYJStock 將股票的重要資訊整合，並且自動化分析，讓投資股票省時簡單！
## 來源
GUI 使用 [kivy](https://github.com/kivy/kivy) 模組  
使用 [yfinance](https://github.com/ranaroussi/yfinance) 查詢股價  
使用 [mplfinance](https://github.com/matplotlib/mplfinance) 生成K線和交易量圖表 
使用 [goodinfo](https://goodinfo.tw) 將股票名稱轉換成股票代碼   
字型使用「jf open 粉圓」由 [justfont](https://github.com/justfont/open-huninn-font) 設計  
圖片素材使用 [flaticon](https://www.flaticon.com)  
## 速率限制
Yahoo Finance API 每小時 2000 次 / 1 IP (約等於 每秒 2次)  
Goodinfo! 台灣股市資訊網 未知  