# plotting.py
import mplfinance as mpf
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def plot_stock_data(data, ax1, ax2, ax_macd, title):
    """
    绘制股票数据的K线图、成交量图和MACD指标图
    :param data: 股票数据
    :param ax1: K线图的坐标轴
    :param ax2: 成交量图的坐标轴
    :param ax_macd: MACD指标图的坐标轴
    :param title: 图表标题
    """
    mpf.plot(
        data,
        type='candle',
        ax=ax1,
        volume=ax2,
        style='yahoo',
        axtitle=title
    )
    # 绘制MACD指标
    ax_macd.plot(data.index, data['DIF'], label='DIF', color='red')
    ax_macd.plot(data.index, data['DEA'], label='DEA', color='blue')
    ax_macd.bar(data.index, data['MACD'], label='MACD', color='green', alpha=0.5)
    # 标记金叉和死叉
    from data_processing import get_golden_cross_data, get_death_cross_data
    golden_cross_data = get_golden_cross_data(data)
    death_cross_data = get_death_cross_data(data)
    if not golden_cross_data.empty:
        ax_macd.scatter(golden_cross_data.index, golden_cross_data['DIF'], marker='^', color='g', s=100, label='MACD Golden Cross')
    if not death_cross_data.empty:
        ax_macd.scatter(death_cross_data.index, death_cross_data['DIF'], marker='v', color='r', s=100, label='MACD Death Cross')
    ax_macd.legend()
def embed_plot(fig, root):
    """
    将Figure对象嵌入到Tkinter窗口
    :param fig: Figure对象
    :param root: Tkinter窗口
    """
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)