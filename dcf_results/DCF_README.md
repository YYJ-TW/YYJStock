## 輸出檔案說明

### 產業查詢 CSV 欄位
- **code**: 股票代碼
- **name**: 股票名稱
- **industry**: 產業別
- **price**: 現價
- **eps**: 使用的 EPS
- **eps_source**: EPS 來源（當前/法人預估）
- **eps_cagr**: EPS CAGR (%)
- **cagr_source**: CAGR 來源（歷史EPS/產業平均/預設值）
- **internal_growth**: 內部成長率 (%)
- **internal_source**: 內部成長率來源
- **dcf_eps**: 基於 EPS CAGR 的 DCF 估值
- **dcf_internal**: 基於內部成長率的 DCF 估值
- **upside_eps**: EPS 法上漲空間 (%)
- **upside_internal**: 內部成長法上漲空間 (%)

### 歷史查詢 CSV 欄位

- **code, name, industry, price**: 現價
- **eps, eps_source**: EPS 來源
- **eps_cagr, cagr_source**: CAGR 及來源
- **internal_growth, internal_source**: 內部成長率及來源
- **dcf_eps**: 基於 EPS CAGR 的 DCF
- **dcf_internal**: 基於內部成長率的 DCF
- **upside_eps, upside_internal**: 兩種方法的上漲空間