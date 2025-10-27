"""
台股 DCF 二階段折現模型估值

用法:
    python3.8 dcf_main.py                   # 顯示可用產業
    python3.8 dcf_main.py 半導體業           # 分析特定產業，產業名稱：csv/twse.csv 或 csv/tpex.csv
    python3.8 dcf_main.py 2330              # 分析單一股票
    python3.8 dcf_main.py watchlist         # 自選股

analyze_industry(industry_name)     分析特定產業，產業名稱：csv/twse.csv 或 csv/tpex.csv
analyze_single(code)                輸入股票代碼查詢單一股票之折現模型估值
watchlist()                         自選股
"""

import sys
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
from stock_data_api import StockDataAPI

"""
產業平均 CAGR (找不到歷史 EPS 時使用)
以下資料僅供參考，缺乏準確性，請手動設定數值
可參考 Global Market Insights 的產業 CAGR 資料：https://www.gminsights.com/
"""
INDUSTRY_CAGR = {
    '半導體業': 0.20,
    '電腦及週邊設備業': 0.12,
    '光電業': 0.10,
    '電子零組件業': 0.15,
    '通信網路業': 0.12,
    '電子通路業': 0.08,
    '資訊服務業': 0.10,
    '其他電子業': 0.10,
    '金融保險業': 0.05,
    '鋼鐵工業': 0.03,
    '橡膠工業': 0.04,
    '汽車工業': 0.05,
    '建材營造業': 0.04,
    '航運業': 0.03,
    '觀光餐旅': 0.04,
    '食品工業': 0.05,
    '紡織纖維': 0.03,
}


def load_stocks_from_csv():
    stocks = []
    
    # 讀取上市股票
    try:
        df = pd.read_csv('csv/twse.csv', skiprows=2, header=None, on_bad_lines='skip')
        for _, row in df.iterrows():
            if len(row) >= 6:
                code = str(row[0]).strip()
                name = str(row[1]).strip()
                industry = str(row[5]).strip() if pd.notna(row[5]) else 'Unknown'
                if code.isdigit() and len(code) == 4:
                    stocks.append({
                        'code': code,
                        'name': name,
                        'market': 'TWSE',
                        'industry': industry
                    })
        print(f"載入 {len(stocks)} 檔上市股票")
    except Exception as e:
        print(f"讀取上市股票失敗: {e}")
    
    # 讀取上櫃股票
    try:
        df = pd.read_csv('csv/tpex.csv', skiprows=2, header=None, on_bad_lines='skip')
        tpex_count = 0
        for _, row in df.iterrows():
            if len(row) >= 6:
                code = str(row[0]).strip()
                name = str(row[1]).strip()
                industry = str(row[5]).strip() if pd.notna(row[5]) else 'Unknown'
                if code.isdigit() and len(code) == 4:
                    stocks.append({
                        'code': code,
                        'name': name,
                        'market': 'TPEX',
                        'industry': industry
                    })
                    tpex_count += 1
        print(f"載入 {tpex_count} 檔上櫃股票")
    except Exception as e:
        print(f"讀取上櫃股票失敗: {e}")
    
    return stocks


def calculate_dcf(current_eps, growth_rate, discount_rate=0.10, mid_term_growth=0.03, 
                  perpetual_growth=0.02, years=10):
    """計算 DCF 合理價值"""
    if not current_eps or not growth_rate or current_eps <= 0:
        return None
    
    EPS0 = current_eps  # 每股參數：最新 EPS
    r = discount_rate
    
    cash_flows = []
    for t in range(1, years + 1):
        if t <= 5:
            cf = EPS0 * (1 + growth_rate) ** t
        else:
            cf = EPS0 * (1 + growth_rate) ** 5 * (1 + mid_term_growth) ** (t - 5)
        cash_flows.append(cf)
    
    present_values = [cf / (1 + r) ** t for t, cf in enumerate(cash_flows, start=1)]
    
    terminal_cf = cash_flows[-1]
    terminal_value = terminal_cf * (1 + perpetual_growth) / (r - perpetual_growth)
    pv_terminal = terminal_value / (1 + r) ** years
    
    fair_value = sum(present_values) + pv_terminal
    return fair_value


def analyze_stock_full(stock, api):
    """
    分析單一股票
    兩種估值結果：樂觀 EPS CAGR / 保守 內部成長率
    """
    stock_data = api.get_stock_data(stock)
    
    if not stock_data:
        return None
    
    # 使用 EPS CAGR 計算 DCF
    eps_cagr = stock_data['eps_cagr']
    if eps_cagr is None or eps_cagr <= 0:
        # 若無歷史 CAGR，使用產業平均
        industry = stock.get('industry', 'Unknown')
        eps_cagr = INDUSTRY_CAGR.get(industry, 0.10)
        cagr_source = f"產業平均({stock.get('industry', 'Unknown')})"
    else:
        cagr_source = stock_data['eps_cagr_source']
    
    dcf_eps = calculate_dcf(stock_data['eps_used'], eps_cagr)
    
    # 使用內部成長率計算 DCF
    internal_growth = stock_data['internal_growth']
    if internal_growth and internal_growth > 0:
        dcf_internal = calculate_dcf(stock_data['eps_used'], internal_growth)
        internal_source = stock_data['internal_growth_source']
    else:
        dcf_internal = None
        internal_source = None
    
    if not dcf_eps or dcf_eps <= 0:
        return None
    
    # 淺在空間 %（上漲空間）
    upside_eps = ((dcf_eps - stock_data['current_price']) / stock_data['current_price']) * 100
    upside_internal = ((dcf_internal - stock_data['current_price']) / stock_data['current_price']) * 100 if dcf_internal else None
    
    return {
        'code': stock['code'],
        'name': stock['name'],
        'industry': stock.get('industry', 'Unknown'),
        'price': round(stock_data['current_price'], 2),
        'eps': round(stock_data['eps_used'], 2),
        'eps_source': stock_data['eps_source'],
        'eps_cagr': round(eps_cagr * 100, 2),
        'cagr_source': cagr_source,
        'internal_growth': round(internal_growth * 100, 2) if internal_growth else None,
        'internal_source': internal_source,
        'dcf_eps': round(dcf_eps, 2),
        'dcf_internal': round(dcf_internal, 2) if dcf_internal else None,
        'upside_eps': round(upside_eps, 2),
        'upside_internal': round(upside_internal, 2) if upside_internal else None,
    }


def show_industries():
    stocks = load_stocks_from_csv()
    
    industries = {}
    for stock in stocks:
        ind = stock.get('industry', 'Unknown')
        if ind not in industries:
            industries[ind] = []
        industries[ind].append(stock['code'])
    
    print("\n" + "="*80)
    print("可用產業分類:")
    print("="*80)
    for ind, codes in sorted(industries.items(), key=lambda x: len(x[1]), reverse=True):
        avg_cagr = INDUSTRY_CAGR.get(ind, 0.10)
        print(f"{ind:<30} {len(codes):>4} 檔 (產業平均CAGR: {avg_cagr*100:>4.0f}%)")
    print("="*80 + "\n")


def analyze_industry(industry_name):
    print(f"\n{'='*100}")
    print(f"分析產業: {industry_name}")
    print(f"{'='*100}\n")
    
    stocks = load_stocks_from_csv()
    api = StockDataAPI()
    
    industry_stocks = [s for s in stocks if s.get('industry') == industry_name]
    
    if not industry_stocks:
        print(f"找不到產業: {industry_name}")
        print("請執行 python3.8 dcf_main.py 查看可用產業")
        return
    
    print(f"共 {len(industry_stocks)} 檔股票")
    industry_cagr = INDUSTRY_CAGR.get(industry_name, 0.10)
    print(f"產業平均 CAGR: {industry_cagr*100}%\n")
    
    # Table Header
    header = f"{'代碼':<6}{'名稱':<8}{'價格':>8}  {'潛在空間%':>10}  {'股票價值':>10}  {'CAGR':>7}  {'內成':>7}  來源"
    print(header)
    print("-" * 95)
    
    results = []
    
    for i, stock in enumerate(industry_stocks, 1):
        print(f"\r分析進度: {i}/{len(industry_stocks)} - {stock['code']} {stock['name']}", 
              end="", flush=True)
        
        result = analyze_stock_full(stock, api)
        
        if result:
            results.append(result)
            
        
            sources = []
            if result['cagr_source']:
                sources.append(result['cagr_source'])
            if result['internal_source'] and result['internal_source'] != '使用CAGR':
                sources.append(result['internal_source'])
            source_str = ', '.join(sources) if sources else 'N/A'
            
            line = (f"{result['code']:<6}"
                   f"{result['name']:<8}"
                   f"{result['price']:>8.2f}  "
                   f"{result['upside_eps']:>9.2f}%  "
                   f"{result['dcf_eps']:>9.2f}  "
                   f"{result['eps_cagr']:>6.1f}%  "
                   f"{result['internal_growth']:>6.1f}%" if result['internal_growth'] else "   N/A")
            
            if result['internal_growth']:
                line += f"  {source_str}"
            else:
                line += f"     N/A  {source_str}"
            
            print(f"\r{line}")
        
        time.sleep(0.5)  # Avoid rate limiting
    
    print("\n" + "="*100)
    
    # 篩選符合條件的股票 (DCF 估值 > 現價)
    eligible_eps = [r for r in results if r['upside_eps'] > 0]
    eligible_internal = [r for r in results if r['upside_internal'] and r['upside_internal'] > 0]
    
    eligible_eps.sort(key=lambda x: x['upside_eps'], reverse=True)
    
    print(f"\n分析完成!")
    print(f"成功分析: {len(results)}/{len(industry_stocks)} 檔")
    print(f"符合條件 (DCF-EPS > 現價): {len(eligible_eps)} 檔")
    print(f"符合條件 (DCF-內成 > 現價): {len(eligible_internal)} 檔")
    
    if eligible_eps:
        print(f"\nTop 20 低估股票 (基於 EPS CAGR):")
        print(f"{'='*80}")
        for stock in eligible_eps[:20]:
            print(f"{stock['code']:<6} {stock['name']:<10} 上漲空間: {stock['upside_eps']:>6.2f}%  "
                  f"CAGR: {stock['eps_cagr']:>5.1f}% ({stock['cagr_source']})")
    
    if results:
        save_results(results, industry_name)


def analyze_single(code):
    stocks = load_stocks_from_csv()
    api = StockDataAPI()
    
    stock = next((s for s in stocks if s['code'] == code), None)
    
    if not stock:
        print(f"找不到股票代碼: {code}")
        return
    
    print(f"\n{'='*80}")
    print(f"DCF 估值分析: {stock['code']} {stock['name']} ({stock['industry']})")
    print(f"{'='*80}\n")
    
    result = analyze_stock_full(stock, api)
    
    if result:
        # 資料來源區塊
        print(f"========== 資料來源 ==========")
        print(f"  EPS:          {result['eps_source']}")
        print(f"  EPS CAGR:     {result['cagr_source']}")
        if result['internal_source']:
            print(f"  內部成長率:    {result['internal_source']}")
        print()
        
        print(f"========== 當前數據 ==========")
        print(f"  現價:         ${result['price']:.2f}")
        print(f"  當前 EPS:     ${result['eps']:.2f}")
        print()
        
        print(f"========== 方法1: EPS CAGR ==========")
        print(f"  1-5年成長率:  {result['eps_cagr']:.2f}%")
        print(f"  6-10年成長率: 3.00%")
        print(f"  折現率:       10.00%")
        print(f"  永續成長率:   2.00%")
        print()
        print(f"  Total Fair Value (per share): ${result['dcf_eps']:.2f}")
        print(f"  潛在報酬空間:                  {result['upside_eps']:+.2f}%")
        print()
        
        if result['dcf_internal'] and result['internal_source']:
            print(f"========== 方法2: 內部成長率 ==========")
            print(f"  1-5年成長率:  {result['internal_growth']:.2f}%")
            print(f"  6-10年成長率: 3.00%")
            print(f"  折現率:       10.00%")
            print(f"  永續成長率:   2.00%")
            print()
            print(f"  Total Fair Value (per share): ${result['dcf_internal']:.2f}")
            print(f"  潛在報酬空間:                  {result['upside_internal']:+.2f}%")
            print()
        
        print(f"========== 評估結論 ==========")
        if result['upside_eps'] > 0:
            print(f"  股票可能被低估")
        else:
            print(f"  股票可能被高估")
        
        print(f"\n{'='*80}\n")
        
        save_single(result)
    else:
        print("分析失敗 - 可能是股票代碼錯誤或是 TWSE API Rate Limit 超出")


def watchlist():
    codes = ['2453', '8103', '6213']
    
    print(f"\n{'='*110}")
    print("自選股分析")
    print(f"{'='*110}\n")
    
    stocks = load_stocks_from_csv()
    api = StockDataAPI()
    
    header = f"{'代碼':<6}{'名稱':<8}{'價格':>8}  {'潛在空間%':>10}  {'股票價值':>10}  {'CAGR':>7}  {'內成':>7}  來源"
    print(header)
    print("-" * 95)
    
    for code in codes:
        stock = next((s for s in stocks if s['code'] == code), None)
        if stock:
            result = analyze_stock_full(stock, api)
            
            if result:
                upside_str = f"{result['upside_eps']:>6.2f}%"
                fair_value_str = f"${result['dcf_eps']:>7.2f}"
                cagr_str = f"{result['eps_cagr']:>5.1f}%"
                internal_str = f"{result['internal_growth']:>5.1f}%" if result['internal_growth'] else "N/A   "
                
                sources = []
                if result['cagr_source']:
                    sources.append(result['cagr_source'])
                if result['internal_source'] and result['internal_source'] != '使用CAGR':
                    sources.append(result['internal_source'])
                source_str = ', '.join(sources) if sources else 'N/A'
                
                line = (f"{result['code']:<6}"
                       f"{result['name']:<8}"
                       f"{result['price']:>8.2f}  "
                       f"{result['upside_eps']:>9.2f}%  "
                       f"{result['dcf_eps']:>9.2f}  "
                       f"{result['eps_cagr']:>6.1f}%  "
                       f"{result['internal_growth']:>6.1f}%" if result['internal_growth'] else "   N/A")
                
                if result['internal_growth']:
                    line += f"  {source_str}"
                else:
                    line += f"     N/A  {source_str}"
                
                print(line)
        
        time.sleep(0.5)
    
    print("="*110 + "\n")


def save_results(results, industry_name):
    if not results:
        return
    
    Path('dcf_results').mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    df = pd.DataFrame(results)
    
    columns_order = [
        'code', 'name', 'industry', 'price', 
        'eps', 'eps_source',
        'eps_cagr', 'cagr_source',
        'internal_growth', 'internal_source',
        'dcf_eps', 'upside_eps',
        'dcf_internal', 'upside_internal'
    ]
    
    df = df[columns_order]
    
    filename = f'dcf_results/{industry_name}_{timestamp}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n結果已保存: {filename}")


def save_single(result):
    Path('dcf_results').mkdir(exist_ok=True)
    history_file = 'dcf_results/analysis_history.csv'
    
    df_new = pd.DataFrame([result])
    df_new['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if Path(history_file).exists():
        df_old = pd.read_csv(history_file, encoding='utf-8-sig')
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    
    df.to_csv(history_file, index=False, encoding='utf-8-sig')
    print(f"已保存到: {history_file}")


def main():
    if len(sys.argv) == 1 or sys.argv[1] == 'list':
        show_industries()
    elif sys.argv[1] == 'watchlist':
        watchlist()
    elif sys.argv[1].isdigit():
        analyze_single(sys.argv[1])
    else:
        analyze_industry(sys.argv[1])


if __name__ == '__main__':
    main()
