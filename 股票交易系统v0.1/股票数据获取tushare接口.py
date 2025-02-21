import tushare as ts
import pandas as pd
def fetch_stock_data(stock_codes, start_date, end_date):
    # 初始化 tushare
    ts.set_token('438682642c64d7140154f9f9bf4c05c0bbef7246d0209b035a8ecf28')
    pro = ts.pro_api()
    stock_data_dict = {}
    for code in stock_codes:
        # 获取单只股票的数据
        data = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
        if data.empty:
            print(f"未获取到 {code} 在 {start_date} 到 {end_date} 的数据，请检查输入。")
            continue
        # 重命名列，以符合 mplfinance 的要求
        data.rename(columns={'trade_date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'vol': 'Volume'}, inplace=True)
        # 将日期列设置为索引，并将日期格式转换为 datetime
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        # 按照日期升序排列
        data.sort_index(inplace=True)
        # 计算MACD指标
        short_ema = data['Close'].ewm(span=12, adjust=False).mean()
        long_ema = data['Close'].ewm(span=26, adjust=False).mean()
        data['DIF'] = short_ema - long_ema
        data['DEA'] = data['DIF'].ewm(span=9, adjust=False).mean()
        data['MACD'] = 2 * (data['DIF'] - data['DEA'])
        # 判断金叉和死叉
        data['macd_golden_cross'] = (data['DIF'] > data['DEA']) & (data['DIF'].shift(1) <= data['DEA'].shift(1))
        data['macd_death_cross'] = (data['DIF'] < data['DEA']) & (data['DIF'].shift(1) >= data['DEA'].shift(1))
        stock_data_dict[code] = data
    return stock_data_dict