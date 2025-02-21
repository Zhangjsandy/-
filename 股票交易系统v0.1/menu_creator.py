import tkinter as tk
from plot_operations import view_all_stocks, view_single_stock, view_stocks_by_days
from backtest_display import run_backtest
def create_menu(root, stock_data_dict):
    menubar = tk.Menu(root)
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="查看", menu=view_menu)
    view_menu.add_command(label="查看所有股票", command=lambda: view_all_stocks(root, stock_data_dict))
    # 查看单支股票
    stock_menu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label="查看单支股票", menu=stock_menu)
    for code in stock_data_dict.keys():
        stock_menu.add_command(label=code, command=lambda c=code: view_single_stock(root, stock_data_dict, c))
    # 查看指定天数的股票 K 线图和MACD图
    days_menu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label="查看指定天数的股票K线图和MACD图", menu=days_menu)
    for days in range(1, 366):
        days_menu.add_command(label=f"{days}天", command=lambda d=days: view_stocks_by_days(root, stock_data_dict, d))
    view_menu.add_command(label="运行回测", command=lambda: run_backtest(root, stock_data_dict))
    root.config(menu=menubar)
    return menubar