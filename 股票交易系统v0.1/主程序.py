import tkinter as tk
import pymysql
from 股票数据获取tushare接口 import fetch_stock_data
from 绘图模块 import plot_kline
from 股票预测模块 import predict_stock_prices
#将数据存入mysql数据库
def insert_stock_data_to_db(stock_data_dict, start_date, end_date):
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
            sql = 'insert ignore into kl(stock_code, trade_date, open_price, high_price, low_price, close_price, volume, start_date, end_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            val = (code, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], start_date, end_date)
            cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
#数据获取与处理
def get_and_process_data():
    stock_codes_input = stock_code_entry.get()
    stock_codes = [code.strip() for code in stock_codes_input.split(',')]
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    stock_data_dict = fetch_stock_data(stock_codes, start_date, end_date)
    insert_stock_data_to_db(stock_data_dict, start_date, end_date)
    plot_kline(stock_data_dict)
    # 调用随机森林预测函数
    predictions = predict_stock_prices(stock_data_dict)
    print("预测结果:", predictions)
root = tk.Tk()
root.title("股票数据输入窗口")
tk.Label(root, text="请输入股票代码，多个代码用逗号分隔").pack()
stock_code_entry = tk.Entry(root)
stock_code_entry.pack()
tk.Label(root, text="请输入起始日期(格式:YYYY-MM-DD)").pack()
start_date_entry = tk.Entry(root)
start_date_entry.pack()
tk.Label(root, text="请输入结束日期(格式:YYYY-MM-DD)").pack()
end_date_entry = tk.Entry(root)
end_date_entry.pack()
tk.Button(root, text="确定", command=get_and_process_data).pack()
root.mainloop()