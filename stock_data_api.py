"""
Stock Data API
Fetch stock data from TWSE official API
"""

import requests
import pandas as pd
from datetime import datetime
import time


class StockDataAPI:
    """Stock data fetcher using official TWSE API"""
    
    def __init__(self):
        self.twse_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self._price_cache = None
        self._pe_cache = None
    
    def _fetch_all_prices(self):
        """Fetch all stock prices from TWSE API"""
        if self._price_cache is not None:
            return self._price_cache
        
        try:
            url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
            res = requests.get(url, headers=self.twse_headers, timeout=10)
            data = res.json()
            
            # Convert to dict for faster lookup
            self._price_cache = {item['Code']: item for item in data}
            return self._price_cache
        except Exception as e:
            print(f"Error fetching prices: {e}")
            return {}
    
    def _fetch_all_pe_ratios(self):
        """Fetch all P/E ratios from TWSE API"""
        if self._pe_cache is not None:
            return self._pe_cache
        
        try:
            url = 'https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL'
            res = requests.get(url, headers=self.twse_headers, timeout=10)
            data = res.json()
            
            # Convert to dict for faster lookup
            self._pe_cache = {item['Code']: item for item in data}
            return self._pe_cache
        except Exception as e:
            print(f"Error fetching P/E ratios: {e}")
            return {}
    
    def get_all_stock_list(self, use_cache=True):
        """
        Get all Taiwan stocks from TWSE official website or local cache
        
        Args:
            use_cache: Use local CSV cache if available
            
        Returns:
            list: List of stock dictionaries with industry info
        """
        import os
        
        stocks = []
        
        # Try to use local cache first
        if use_cache:
            if os.path.exists('csv/twse.csv'):
                try:
                    df = pd.read_csv('csv/twse.csv', encoding='utf-8')
                    for idx, row in df.iterrows():
                        if len(row) >= 6:
                            code = str(row[0]).strip()
                            name = str(row[1]).strip()
                            industry = str(row[5]).strip() if len(row) > 5 else 'Unknown'
                            if code.isdigit() and len(code) == 4:
                                stocks.append({
                                    'code': code,
                                    'name': name,
                                    'market': 'TWSE',
                                    'industry': industry
                                })
                    print(f"Loaded {len(stocks)} TWSE stocks from cache")
                except Exception as e:
                    print(f"Error loading TWSE cache: {e}")
            
            if os.path.exists('csv/tpex.csv'):
                try:
                    df = pd.read_csv('csv/tpex.csv', encoding='utf-8')
                    tpex_count = 0
                    for idx, row in df.iterrows():
                        if len(row) >= 6:
                            code = str(row[0]).strip()
                            name = str(row[1]).strip()
                            industry = str(row[5]).strip() if len(row) > 5 else 'Unknown'
                            if code.isdigit() and len(code) == 4:
                                stocks.append({
                                    'code': code,
                                    'name': name,
                                    'market': 'TPEX',
                                    'industry': industry
                                })
                                tpex_count += 1
                    print(f"Loaded {tpex_count} TPEX stocks from cache")
                except Exception as e:
                    print(f"Error loading TPEX cache: {e}")
            
            if stocks:
                return stocks
        
        # Fallback: try to fetch from TWSE (with retry)
        print("Fetching from TWSE website (may be slow)...")
        
        for retry in range(3):
            try:
                url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
                res = requests.get(url, headers=self.twse_headers, timeout=30)
                res.encoding = 'big5'
                df = pd.read_html(res.text)[0]
                df.columns = df.iloc[0]
                df = df.iloc[1:]
                df = df.dropna(thresh=3, axis=0)
                
                for idx, row in df.iterrows():
                    code_name = row['有價證券代號及名稱']
                    industry = row.get('產業別', 'Unknown')
                    if isinstance(code_name, str) and '  ' in code_name:
                        parts = code_name.split('  ')
                        if len(parts) >= 2:
                            code, name = parts[0], parts[1]
                            if code.isdigit() and len(code) == 4:
                                stocks.append({
                                    'code': code,
                                    'name': name,
                                    'market': 'TWSE',
                                    'industry': industry
                                })
                print(f"Fetched {len(stocks)} TWSE stocks")
                break
            except Exception as e:
                print(f"Retry {retry+1}/3 - Error fetching TWSE stocks: {e}")
                if retry < 2:
                    time.sleep(5)
        
        # TPEX with retry
        for retry in range(3):
            try:
                url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
                res = requests.get(url, headers=self.twse_headers, timeout=30)
                res.encoding = 'big5'
                df = pd.read_html(res.text)[0]
                df.columns = df.iloc[0]
                df = df.iloc[1:]
                df = df.dropna(thresh=3, axis=0)
                
                tpex_count = 0
                for idx, row in df.iterrows():
                    code_name = row['有價證券代號及名稱']
                    industry = row.get('產業別', 'Unknown')
                    if isinstance(code_name, str) and '  ' in code_name:
                        parts = code_name.split('  ')
                        if len(parts) >= 2:
                            code, name = parts[0], parts[1]
                            if code.isdigit() and len(code) == 4:
                                stocks.append({
                                    'code': code,
                                    'name': name,
                                    'market': 'TPEX',
                                    'industry': industry
                                })
                                tpex_count += 1
                print(f"Fetched {tpex_count} TPEX stocks")
                break
            except Exception as e:
                print(f"Retry {retry+1}/3 - Error fetching TPEX stocks: {e}")
                if retry < 2:
                    time.sleep(5)
        
        return stocks
    
    def get_current_price(self, code):
        """
        Get current stock price from TWSE API
        
        Args:
            code: Stock code (e.g., '2330')
            
        Returns:
            float: Current price or None
        """
        try:
            prices = self._fetch_all_prices()
            if code in prices:
                price_str = prices[code]['ClosingPrice']
                return float(price_str.replace(',', ''))
            return None
        except:
            return None
    
    def get_pe_ratio(self, code):
        """
        Get P/E ratio from TWSE API
        
        Args:
            code: Stock code
            
        Returns:
            float: P/E ratio or None
        """
        try:
            pe_data = self._fetch_all_pe_ratios()
            if code in pe_data:
                pe_str = pe_data[code]['PEratio']
                if pe_str and pe_str != '-':
                    return float(pe_str)
            return None
        except:
            return None
    
    def calculate_current_eps(self, code):
        """
        Calculate current EPS from price and P/E ratio
        EPS = Price / PE
        
        Args:
            code: Stock code
            
        Returns:
            float: Calculated EPS or None
        """
        try:
            price = self.get_current_price(code)
            pe = self.get_pe_ratio(code)
            
            if price and pe and pe > 0:
                eps = price / pe
                return float(eps)
            return None
        except:
            return None
    
    def get_eps_history_finmind(self, code, years=5):
        """
        從 FinMind API 獲取歷史年度 EPS
        
        Args:
            code: 股票代碼
            years: 年數
            
        Returns:
            DataFrame with ['Year', 'EPS'] or None
        """
        try:
            current_year = datetime.now().year
            url = 'https://api.finmindtrade.com/api/v4/data'
            params = {
                'dataset': 'TaiwanStockFinancialStatements',
                'data_id': code,
                'start_date': f'{current_year - years - 1}-01-01',
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'data' not in data or len(data['data']) == 0:
                return None
            
            df = pd.DataFrame(data['data'])
            
            # 只取 EPS
            eps_df = df[df['type'] == 'EPS'].copy()
            
            if eps_df.empty:
                return None
            
            # 提取年份和月份
            eps_df['date'] = pd.to_datetime(eps_df['date'])
            eps_df['Year'] = eps_df['date'].dt.year
            eps_df['Month'] = eps_df['date'].dt.month
            eps_df['EPS'] = pd.to_numeric(eps_df['value'], errors='coerce')
            
            # 將四季 EPS 加總成年度 EPS
            annual_eps = eps_df.groupby('Year')['EPS'].sum().reset_index()
            
            # 排除當年度因為只有部分季度數據
            annual_eps = annual_eps[annual_eps['Year'] < current_year]
            
            # 過濾正值 EPS
            annual_eps = annual_eps[annual_eps['EPS'] > 0]
            
            # 取最近 N+1 年來計算 N 年的 CAGR
            # 例如：要計算5年 CAGR 需要6個數據點 (2019-2024)
            annual_eps = annual_eps.tail(years + 1)
            
            if len(annual_eps) < 2:
                return None
            
            return annual_eps[['Year', 'EPS']]
            
        except Exception as e:
            return None
    
    def get_internal_growth_rate(self, code):
        """
        計算內部成長率（基本成長率）
        使用 PE 和 PB 比率計算 ROE
        ROE = (1/PB) / (1/PE) = PE/PB
        內部成長率 = ROE × 盈餘保留率
        
        Args:
            code: 股票代碼
            
        Returns:
            float: 內部成長率 or None
        """
        try:
            pe = self.get_pe_ratio(code)
            
            # 從 TWSE API 獲取 PB 比率
            pe_data = self._fetch_all_pe_ratios()
            if code not in pe_data:
                return None
            
            pb_str = pe_data[code].get('PBratio', None)
            if not pb_str or pb_str == '-':
                return None
            
            pb = float(pb_str)
            
            if pe and pb and pe > 0 and pb > 0:
                # ROE = PB / PE
                # 因為 ROE = EPS/BPS = (Price/PE)/(Price/PB) = PB/PE
                roe = pb / pe
                
                # 假設盈餘保留率 70%（保守）
                retention_rate = 0.7
                internal_growth = roe * retention_rate
                
                # 限制在合理範圍 (0% ~ 50%)
                if 0 < internal_growth < 0.50:
                    return float(internal_growth)
            
            return None
            
        except Exception as e:
            return None
    
    def get_analyst_forecast_eps(self, code):
        """
        TODO: 獲取法人預估 EPS
        
        Args:
            code: Stock code
            
        Returns:
            float: Forecast EPS or None
        """
        return None
    
    def calculate_eps_cagr(self, eps_history):
        """
        Calculate EPS Compound Annual Growth Rate
        
        Args:
            eps_history: DataFrame with columns ['Year', 'EPS']
            
        Returns:
            float: CAGR or None
        """
        if eps_history is None or len(eps_history) < 2:
            return None
        
        if (eps_history['EPS'] <= 0).any():
            return None
        
        eps_history = eps_history.sort_values('Year')
        first_eps = eps_history['EPS'].iloc[0]
        last_eps = eps_history['EPS'].iloc[-1]
        n_years = len(eps_history) - 1
        
        if first_eps <= 0 or last_eps <= 0:
            return None
        
        cagr = (last_eps / first_eps) ** (1 / n_years) - 1
        
        # Set reasonable range (-50% to 100%)
        if cagr < -0.5 or cagr > 1.0:
            return None
        
        return float(cagr)
    
    def get_stock_data(self, stock_info, default_cagr=0.10, custom_cagr_map=None):
        """
        獲取股票完整數據供 DCF 分析
        
        Args:
            stock_info: 股票資訊字典
            default_cagr: 預設 CAGR (10%)
            custom_cagr_map: 自訂 CAGR 映射
            
        Returns:
            dict: 完整股票數據或 None
        """
        code = stock_info['code']
        
        data = {
            'code': code,
            'name': stock_info['name'],
            'market': stock_info['market'],
            'current_price': None,
            'current_eps': None,
            'forecast_eps': None,
            'eps_used': None,
            'eps_source': None,
            'eps_cagr': None,
            'eps_cagr_source': None,
            'internal_growth': None,
            'internal_growth_source': None,
            'eps_history': None,
        }
        
        # 獲取當前股價
        current_price = self.get_current_price(code)
        if current_price is None or current_price <= 0:
            return None
        data['current_price'] = current_price
        
        # 計算當前 EPS (從本益比)
        current_eps = self.calculate_current_eps(code)
        if current_eps is None or current_eps <= 0:
            return None
        data['current_eps'] = current_eps
        
        # 嘗試獲取法人預估 EPS
        forecast_eps = self.get_analyst_forecast_eps(code)
        data['forecast_eps'] = forecast_eps
        
        # 決定使用哪個 EPS
        if forecast_eps and forecast_eps > 0:
            data['eps_used'] = forecast_eps
            data['eps_source'] = '法人預估'
        else:
            data['eps_used'] = current_eps
            data['eps_source'] = '當前'
        
        # 計算 EPS CAGR（歷史數據）
        if custom_cagr_map and code in custom_cagr_map:
            data['eps_cagr'] = custom_cagr_map[code]
            data['eps_cagr_source'] = '自訂'
        else:
            eps_history = self.get_eps_history_finmind(code, years=5)
            
            if eps_history is not None and len(eps_history) >= 2:
                data['eps_history'] = eps_history
                cagr = self.calculate_eps_cagr(eps_history)
                # 檢查 CAGR 是否合理（至少 -20%）
                if cagr is not None and cagr >= -0.20:
                    data['eps_cagr'] = cagr
                    data['eps_cagr_source'] = '歷史EPS'
                else:
                    data['eps_cagr'] = default_cagr
                    data['eps_cagr_source'] = '預設值'
            else:
                data['eps_cagr'] = default_cagr
                data['eps_cagr_source'] = '預設值'
        
        # 計算內部成長率（ROE based）
        internal_growth = self.get_internal_growth_rate(code)
        if internal_growth is not None and internal_growth > 0:
            data['internal_growth'] = internal_growth
            data['internal_growth_source'] = 'TWSE-ROE'
        else:
            # 無法計算則設為 None（不使用CAGR回退）
            data['internal_growth'] = None
            data['internal_growth_source'] = None
        
        # 修正 CAGR 來源標示
        if data['eps_cagr_source'] == '歷史EPS':
            data['eps_cagr_source'] = 'FinMind'
        
        # 修正 EPS 來源標示
        if data['eps_source'] == '當前':
            data['eps_source'] = 'TWSE-本益比'
        elif data['eps_source'] == '法人預估':
            data['eps_source'] = 'FinMind-預估'
        
        return data
