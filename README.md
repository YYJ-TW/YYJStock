# YYJStock
股市資料一把抓，由軟體協助選股、買進和賣出訊號分析，節省研究時間！

## 專案結構
```
YYJStock/
├── dcf_main.py                  # DCF 主程式（產業分析/單一股票/自選股）
├── stock_data_api.py            # 股票資料 API（TWSE + FinMind）
├── 2_stage_dcf.py               # 手動 DCF 計算
├── csv/                         # 股票列表 CSV
└── dcf_results/                 # 所有 DCF 分析結果（產業 + 單一股票）
```

## DCF 二階段折現模型估值
**輸入參數**
- **每股參數 $EPS$**: 當前 EPS（股價 / 本益比）
- **1-5 年成長率**: 這部分有多種參數可選，主要是 EPS CAGR 或是 公司內部成長率
- **6-10 年成長率**: 較難預估，通常是填 GDP 的長期成長率 2~3%
- **折現率 $r$**: 10% 股市平均回報率大約是 7~10%
- **永續成長率 $g_\infty$**: 2% 不超過 GDP 數值

公司現值（per-share）PV：
```math
PV = \sum_{t=1}^5 \frac{EPS_0(1+gCAGR)^t}{(1+r)^t}+\sum_{t=6}^{10}\frac{EPS_0(1+gCAGR)^5(1+gGDP)^{t-5})}{(1+r)^t}+\frac{TV_{10}}{(1+r)^{10}}
```

使用 Gordon Growth Model 計算 Terminal Value：
```math
TV_{10}=\frac{EPS_{10}(1+g_\infty)}{r-g_\infty} \qquad 
EPS_{10}=EPS_0 (1+gCGAR)^5(1+gGDP)^5
```

Compound Annual Growth Rate（CAGR）年複合成長率：
```math
CAGR(\%)=\frac{Ending Value}{Beginning Value}^{1/t}-1
```

[手動 DCF 計算器](2_stage_dcf.py)

### 使用方法
```bash
python3.8 dcf_main.py           # 顯示所有可用產業
python3.8 dcf_main.py 半導體業   # 分析特定產業（例如：半導體業）
python3.8 dcf_main.py 2330      # 分析單一股票（例如：台積電）
python3.8 dcf_main.py watchlist # 快速測試 10 檔大型股
```
注意：產業平均 CAGR 請勿參考，請手動設定數值。可參考 Global Market Insights 的產業 CAGR 資料：https://www.gminsights.com/

## DCF 參數選擇
系統提供兩種估值方法比較：

### 方法1: EPS CAGR 法
- 使用過去5年實際 EPS 複合成長率
- 資料來源：FinMind API（四季 EPS 加總）
- 適合：過去 5 年成長穩定的公司

### 方法2: 內部成長率法 (股價淨值比/本益比) x 70% = ROE x 保留率
- 使用 ROE × 盈餘保留率
- 資料來源：TWSE ROE 財報數據
- 適合：高 ROE 的公司

### 輸出範例
#### 單一股票分析
```
========== 資料來源 ==========
  EPS:          TWSE-本益比
  EPS CAGR:     FinMind
  內部成長率:    TWSE-ROE

========== 當前數據 ==========
  現價:         $42.00
  當前 EPS:     $3.51

========== 方法1: EPS CAGR ==========
  1-5年成長率:  11.00%
  6-10年成長率: 3.00%
  折現率:       10.00%
  永續成長率:   2.00%

  Total Fair Value (per share): $66.86
  潛在報酬空間:                  +59.19%

========== 方法2: 內部成長率 ==========
  1-5年成長率:  11.17%
  6-10年成長率: 3.00%
  折現率:       10.00%
  永續成長率:   2.00%

  Total Fair Value (per share): $67.31
  潛在報酬空間:                  +60.27%

========== 評估結論 ==========
  股票可能被低估
```

#### 產業分析
```
分析產業: 半導體業
共 175 檔股票

代碼   名稱       價格     DCF-EPS  DCF-內成   EPS CAGR   內成長率   來源
-----------------------------------------------------------------------------------
分析進度: 1/175
2330   台積電     1450.00  2029.51  2029.51    27.7%(歷史EPS)  27.7%(使用CAGR)  當前
...

符合條件 (DCF > 現價): 85/175 檔

Top 20 低估股票:
2330   台積電     上漲空間:  40.00%  CAGR: 27.7% (歷史EPS)
...

結果已保存: dcf_results/半導體業_20251027_123456.csv
```

### 輸出檔案
所有結果統一保存在 `dcf_results/` 資料夾：

- `dcf_results/{產業}_{時間}.csv` - 產業分析結果
- `dcf_results/analysis_history.csv` - 單一股票分析歷史

## 舊版功能
### 股票資訊來源
- [台灣證券交易所](https://www.twse.com.tw)
- [Goodinfo! 台灣股市資訊網](https://goodinfo.tw)

### 指令
```python3 cli.py -h``` 獲得指令列表  
```python3 cli.py 2330 5 10``` 搜尋台積電財報資料

## 免責聲明
⚠️ **本工具僅供學習與研究使用。投資有風險，請審慎評估。**

## 聯絡資訊
- Email: `yyj@yyjstudio.com`
- Discord: `@yyj_tw`