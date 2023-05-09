# YYJStock
## 簡介
[English Version](en_US.md)  
股市資料一把抓，由軟體協助選股、買進和賣出訊號分析，節省研究時間！
## 功能介紹
- 股價、財報資訊查詢
- Prophet AI 股價預測
## 來源
### 股票資訊來源
- [台灣證券交易所](https://www.twse.com.tw) 證券代號及名稱表格  
- [Yahoo Finance API](https://github.com/ranaroussi/yfinance) 股價資訊  
- [Goodinfo! 台灣股市資訊網](https://goodinfo.tw) 財報資訊  
### 字體與圖片素材
- [jf open 粉圓](https://github.com/justfont/open-huninn-font) 由 justfont 設計的字型
- [flaticon](https://www.flaticon.com) 圖片素材  
## 指令
```python3 cli.py -h``` 獲得指令列表  
```python3 cli.py 2330 5 10``` 搜尋股票代碼 2330 (台積電)，第 5 列的財報資料(漲跌)，取得 10 年的資料。
## 速率限制
Yahoo Finance API 每小時 2000 次 / 1 IP (約等於 每秒 2次)  
Goodinfo! 台灣股市資訊網 未知  
