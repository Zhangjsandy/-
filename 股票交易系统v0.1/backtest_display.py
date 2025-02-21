import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from 回测模块 import backtest
def run_backtest(root, stock_data_dict):
    backtest_results = backtest(stock_data_dict)
    result_window = tk.Toplevel(root)
    result_window.title("回测结果")
    text = tk.Text(result_window)
    text.pack()
    for code, result in backtest_results.items():
        text.insert(tk.END, f"股票代码: {code}\n")
        text.insert(tk.END, f"初始资金: 100000\n")
        text.insert(tk.END, f"最终资金: {result['final_capital']:.2f}\n")
        text.insert(tk.END, f"总收益率: {result['final_return'] * 100:.2f}%\n")
        text.insert(tk.END, f"夏普比率: {result['sharpe_ratio']:.2f}\n")
        text.insert(tk.END, f"最大回撤: {result['max_drawdown'] * 100:.2f}%\n")
        text.insert(tk.END, "交易记录:\n")
        for trade in result['trades']:
            text.insert(tk.END, f"{trade[0]} at {trade[1]} with price {trade[2]:.2f}\n")
        text.insert(tk.END, "持仓数量变化记录:\n")
        for change in result['position_changes']:
            text.insert(tk.END, f"{change[0]}: {change[1]:.2f}\n")
        text.insert(tk.END, "\n")
        # 绘制买点分布
        fig1, ax1 = plt.subplots()
        result['buy_distribution'].plot(kind='bar', ax=ax1)
        ax1.set_title(f'{code} 买点分布')
        ax1.set_xlabel('价格区间')
        ax1.set_ylabel('买点数量')
        canvas1 = FigureCanvasTkAgg(fig1, master=result_window)
        canvas1.draw()
        canvas1.get_tk_widget().pack()
        # 绘制买卖频谱
        fig2, ax2 = plt.subplots()
        result['buy_counts'].plot(kind='line', ax=ax2, label='买入次数')
        result['sell_counts'].plot(kind='line', ax=ax2, label='卖出次数')
        ax2.set_title(f'{code} 买卖频谱')
        ax2.set_xlabel('时间（月）')
        ax2.set_ylabel('买卖次数')
        ax2.legend()
        canvas2 = FigureCanvasTkAgg(fig2, master=result_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack()
        # 绘制资产变化趋势图
        fig3, ax3 = plt.subplots()
        ax3.plot(result['capital_history'])
        ax3.set_title(f'{code} 资产变化趋势')
        ax3.set_xlabel('时间')
        ax3.set_ylabel('资产价值')
        canvas3 = FigureCanvasTkAgg(fig3, master=result_window)
        canvas3.draw()
        canvas3.get_tk_widget().pack()