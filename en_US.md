# YYJStock
## Introduction
[Chinese Version](README.md)  
Capture stock market data and analyze stock selection, buy and sell signals with software assistance to save research time!
## Features
- Stock price and financial information lookup
- Prophet AI stock price prediction
## Sources
### Stock Information Sources
- [Taiwan Stock Exchange](https://www.twse.com.tw) for stock code and name data  
- [Yahoo Finance API](https://github.com/ranaroussi/yfinance) for stock price information    
- [Goodinfo! Taiwan Stock Market Information](https://goodinfo.tw) for financial information   
### Fonts and Image Assets
- [jf open-huninn](https://github.com/justfont/open-huninn-font) font designed by justfont
- [flaticon](https://www.flaticon.com) for icon assets  
## Commands
```python3 cli.py -h``` Get a list of available commands    
```python3 cli.py 2330 5 10``` Search for stock code 2330 (TSMC), financial data for the 5th row (price change), and retrieve data for 10 years.  
## Rate Limit
Yahoo Finance API: 2000 requests per hour per IP (approximately 2 requests per second)  
Goodinfo! Taiwan Stock Market Information: Unknown  
