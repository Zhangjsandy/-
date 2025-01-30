#导入数据获取模块
import tushare as ts
import pandas as pd
#导入绘图模块
import mplfinance as mpf
def fetch_stock_data(stock_codes, start_date, end_date):
    # 初始化 tushare
    ts.set_token('438682642c64d7140154f9f9bf4c05c0bbef7246d0209b035a8ecf28')  # 请将 your_tushare_token 替换为你在 tushare 注册后获得的 token
    pro = ts.pro_api()
    all_data = pd.DataFrame()
    for code in stock_codes:
        # 获取单只股票的数据
        data = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
        # 重命名列，以符合 mplfinance 的要求
        data.rename(columns={'trade_date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)
        # 将日期列设置为索引，并将日期格式转换为 datetime
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        # 按照日期升序排列
        data.sort_index(inplace=True)
        all_data = pd.concat([all_data, data], axis=0)
    return all_data
def plot_kline(data):
    # 绘制 K 线图
    mpf.plot(data, type='candle', style='yahoo', title='Stock K-line Chart', ylabel='Price', volume=True)
def main():
    # 多个股票代码，例如：茅台和五粮液
    stock_codes = ['600519.SH', '000858.SZ']
    start_date = '2024-01-01'
    end_date = '2025-01-02'
    # 获取股票数据
    stock_data = fetch_stock_data(stock_codes, start_date, end_date)
    # 绘制 K 线图
    plot_kline(stock_data)
if __name__ == "__main__":
    main()