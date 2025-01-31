import tushare as ts
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import pymysql
def fetch_stock_data(stock_codes, start_date, end_date):
    # 初始化 tushare
    ts.set_token('438682642c64d7140154f9f9bf4c05c0bbef7246d0209b035a8ecf28')
    pro = ts.pro_api()
    stock_data_dict = {}
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
        stock_data_dict[code] = data
    return stock_data_dict
def plot_kline(stock_data_dict):
    num_stocks = len(stock_data_dict)
    fig, axes = mpf.plot(
        stock_data_dict[list(stock_data_dict.keys())[0]],
        type='candle',
        style='yahoo',
        title='Multiple Stock K-line Chart',
        ylabel='Price',
        volume=True,
        returnfig=True
    )
    for i, (code, data) in enumerate(list(stock_data_dict.items())[1:], start=1):
        ax = axes[0] if i == 1 else axes[2 * (i - 1)]
        mpf.plot(
            data,
            type='candle',
            ax=ax,
            volume=axes[2 * i],
            style='yahoo',
            axtitle=code
        )
    plt.show()
def insert_stock_data_to_db(stock_data_dict,start_date,end_date):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='10000popopo',
        database='mysql',
    )
    cursor = conn.cursor()
    for code, data in stock_data_dict.items():
        for index, row in data.iterrows():
            sql = 'insert into kl(stock_code,trade_date,open_price,high_price,low_price,close_price,volume,start_date,end_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            val=(code,index.strftime('%Y-%m-%d'),row['Open'],row['High'],row['Low'],row['Close'],row['Volume'],start_date,end_date)
            cursor.execute(sql, val)
    conn.commit()
 #   sql1 = 'select * from kl'
 #   cursor.execute(sql1)
    cursor.close()
    conn.close()
def main():
    # 多个股票代码，例如：茅台和五粮液
    stock_codes = ['600162.SH','600665.SH']
    start_date = '2024-01-01'
    end_date = '2025-01-02'
    # 获取股票数据
    stock_data_dict = fetch_stock_data(stock_codes, start_date, end_date)
    insert_stock_data_to_db(stock_data_dict,start_date,end_date)
    # 绘制 K 线图
    plot_kline(stock_data_dict)
if __name__ == "__main__":
    main()