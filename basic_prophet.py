import prophet # 股票預測模型
import numpy as np # 多維陣列與矩陣運算
import pandas as pd # 建立數據
import yfinance as yf # 股價資訊
import matplotlib.pyplot as plt # 圖表繪製

stock = input('輸入股票代碼(格式：2330.TW)：')
start = input('輸入開始日期(格式：2022-01-23)：')
end = input('輸入結束日期(格式：2023-01-23)：')
periods = int(input('預測未來股價的天數：'))
price = yf.download(stock, start=start, end=end)
print(price)

plt.style.use('ggplot')
price['Adj Close'].plot(figsize=(10,6)) # 以Adj Close的資料繪製圖表 圖形大小figsize=(寬,高)

train = pd.DataFrame(price['Adj Close']).reset_index().rename(columns={'Date':'ds', 'Adj Close':'y'}) # 建立時間(ds)對應的收盤價(y)數據
train.head()

train['ds'] = train['ds'].dt.tz_localize(None) # 移除timezone
train['y'] = np.log(train['y']) # 計算y的自然對數 y代表Adj Close，可以理解成收盤價

model = prophet.Prophet() # 定義模型
model.fit(train) # 訓練模型
future = model.make_future_dataframe(periods=periods) # 預測未來的股價
forecast = model.predict(future)
forecast.head()
figure=model.plot(forecast)
plt.show() # 顯示圖表