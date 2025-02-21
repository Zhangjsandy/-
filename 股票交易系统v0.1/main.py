import tkinter as tk
from menu_creator import create_menu
from plot_operations import view_all_stocks
def plot_kline(stock_data_dict):
    root = tk.Tk()
    root.title("股票K线图窗口")
    create_menu(root, stock_data_dict)
    # 初始显示全部股票
    view_all_stocks(root, stock_data_dict)
    root.mainloop()
if __name__ == "__main__":
    # 假设这里有股票数据字典 stock_data_dict
    stock_data_dict = {}
    plot_kline(stock_data_dict)