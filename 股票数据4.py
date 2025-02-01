import tushare as ts
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import pymysql
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    root = tk.Tk()
    root.title("股票K线图窗口")
    # 创建菜单栏
    menubar = tk.Menu(root)
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="查看", menu=view_menu)
    def view_all_stocks():
        num_stocks = len(stock_data_dict)
    #创建figure对象
        fig, axes = plt.subplots(num_stocks,ncols=2, figsize=(12, 6 * num_stocks), gridspec_kw={'width_ratios': [3, 1]}
        )
    #查看全部股票
        for i, (code, data) in enumerate(stock_data_dict.items()):
            if num_stocks==1:
                ax1=axes[0]
                ax2=axes[1]
            else:
                ax1=axes[i,0]
                ax2=axes[i,1]
            mpf.plot(
                data,
                type='candle',
                ax=ax1,
                volume=ax2,
                style='yahoo',
                axtitle=code
            )
        #删除之前的绘图
            for widget in root.winfo_children():
                if isinstance(widget,tk.Canvas):
                    widget.destroy()
        # 将Figure对象嵌入到Tkinter窗口
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    view_menu.add_command(label="查看所有股票", command=view_all_stocks)
    #查看单支股票
    stock_menu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label="查看单支股票",menu=stock_menu)
    for code in stock_data_dict.keys():
        def view_single_stock(code=code):
            data = stock_data_dict[code]
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6),
                                      gridspec_kw={'width_ratios': [3, 1]}
                                      )
            ax1=axes[0]
            ax2=axes[1]
            mpf.plot(data, type='candle', ax=ax1, volume=ax2, style='yahoo', axtitle=code)
            for widget in root.winfo_children():
                if isinstance(widget,tk.Canvas):
                    widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        stock_menu.add_command(label=code, command=view_single_stock)
    root.config(menu=menubar)
    #初始显示全部股票
    view_all_stocks()
    root.mainloop()
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
            sql = 'insert ignore into kl(stock_code,trade_date,open_price,high_price,low_price,close_price,volume,start_date,end_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            val=(code,index.strftime('%Y-%m-%d'),row['Open'],row['High'],row['Low'],row['Close'],row['Volume'],start_date,end_date)
            cursor.execute(sql, val)
    conn.commit()
 #   sql1 = 'select * from kl'
 #   cursor.execute(sql1)
    cursor.close()
    conn.close()
def main():
    # 多个股票代码，例如：茅台和五粮液
    stock_codes_input=input("请输入股票代码，多个代码用逗号分隔(例如:600665.SH，600162.SH):")
    stock_codes = [code.strip() for code in stock_codes_input.split('，')]
    start_date = input("请输入起始日期(格式:YYYY-MM-DD):")
    end_date = input("请输入结束日期(格式:YYYY-MM-DD):")
    # 获取股票数据
    stock_data_dict = fetch_stock_data(stock_codes, start_date, end_date)
    #将数据存入数据库
    insert_stock_data_to_db(stock_data_dict,start_date,end_date)
    # 绘制 K 线图
    plot_kline(stock_data_dict)
if __name__ == "__main__":
    main()