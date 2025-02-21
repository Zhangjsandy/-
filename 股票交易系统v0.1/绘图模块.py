import mplfinance as mpf
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from 股票预测模块 import predict_stock_prices
def plot_kline(stock_data_dict):
    root = tk.Tk()
    root.title("股票K线图窗口")
    # 创建菜单栏
    menubar = tk.Menu(root)
    view_menu = tk.Menu(menubar, tearoff=0)#tearoff是否有分割线
    menubar.add_cascade(label="查看", menu=view_menu)
    def view_all_stocks():
        num_stocks = len(stock_data_dict)
        # 创建figure对象，为MACD图留出额外空间
        fig, axes = plt.subplots(num_stocks, ncols=3, figsize=(18, 6 * num_stocks), gridspec_kw={'width_ratios': [3, 1, 1]})
        # 查看全部股票
        for i, (code, data) in enumerate(stock_data_dict.items()):
            if num_stocks == 1:
                ax1 = axes[0]
                ax2 = axes[1]
                ax_macd = axes[2]
            else:
                ax1 = axes[i, 0]
                ax2 = axes[i, 1]
                ax_macd = axes[i, 2]
            mpf.plot(
                data,
                type='candle',
                ax=ax1,
                volume=ax2,
                style='yahoo',
                axtitle=code
            )
            # 绘制MACD指标
            ax_macd.plot(data.index, data['DIF'], label='DIF', color='red')
            ax_macd.plot(data.index, data['DEA'], label='DEA', color='blue')
            ax_macd.bar(data.index, data['MACD'], label='MACD', color='green', alpha=0.5)#alpha为透明度
            # 标记金叉和死叉
            golden_cross_data = data[data['macd_golden_cross']]
            death_cross_data = data[data['macd_death_cross']]
            if not golden_cross_data.empty:
                ax_macd.scatter(golden_cross_data.index, golden_cross_data['DIF'], marker='^', color='g', s=100, label='MACD Golden Cross')
            if not death_cross_data.empty:
                ax_macd.scatter(death_cross_data.index, death_cross_data['DIF'], marker='v', color='r', s=100, label='MACD Death Cross')
            ax_macd.legend()
        # 删除之前的绘图
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        # 将Figure对象嵌入到Tkinter窗口
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    view_menu.add_command(label="查看所有股票", command=view_all_stocks)
    # 查看单支股票
    stock_menu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label="查看单支股票", menu=stock_menu)
    for code in stock_data_dict.keys():
        def view_single_stock(code=code):
            data = stock_data_dict[code]
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), gridspec_kw={'width_ratios': [3, 1, 1]})
            ax1 = axes[0]
            ax2 = axes[1]
            ax_macd = axes[2]
            mpf.plot(data, type='candle', ax=ax1, volume=ax2, style='yahoo', axtitle=code)
            # 绘制MACD指标
            ax_macd.plot(data.index, data['DIF'], label='DIF', color='red')
            ax_macd.plot(data.index, data['DEA'], label='DEA', color='blue')
            ax_macd.bar(data.index, data['MACD'], label='MACD', color='green', alpha=0.5)
            # 标记金叉和死叉
            golden_cross_data = data[data['macd_golden_cross']]
            death_cross_data = data[data['macd_death_cross']]
            if not golden_cross_data.empty:
                ax_macd.scatter(golden_cross_data.index, golden_cross_data['DIF'], marker='^', color='g', s=100, label='MACD Golden Cross')
            if not death_cross_data.empty:
                ax_macd.scatter(death_cross_data.index, death_cross_data['DIF'], marker='v', color='r', s=100, label='MACD Death Cross')
            ax_macd.legend()
            for widget in root.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        stock_menu.add_command(label=code, command=view_single_stock)
    # 查看指定天数的股票 K 线图和MACD图
    days_menu = tk.Menu(view_menu, tearoff=0)
    view_menu.add_cascade(label="查看指定天数的股票K线图和MACD图", menu=days_menu)
    for days in range(1, 366):
        def view_stocks_by_days(days=days):
            num_stocks = len(stock_data_dict)
            fig, axes = plt.subplots(num_stocks, ncols=3, figsize=(18, 6 * num_stocks), gridspec_kw={'width_ratios': [3, 1, 1]})
            for i, (code, data) in enumerate(stock_data_dict.items()):
                recent_data = data.iloc[-days:]
                if num_stocks == 1:
                    ax1 = axes[0]
                    ax2 = axes[1]
                    ax_macd = axes[2]
                else:
                    ax1 = axes[i, 0]
                    ax2 = axes[i, 1]
                    ax_macd = axes[i, 2]
                mpf.plot(
                    recent_data,
                    type='candle',
                    ax=ax1,
                    volume=ax2,
                    style='yahoo',
                    axtitle=f"{code} ({days}天)"
                )
                # 绘制指定天数的MACD指标
                ax_macd.plot(recent_data.index, recent_data['DIF'], label='DIF', color='red')
                ax_macd.plot(recent_data.index, recent_data['DEA'], label='DEA', color='blue')
                ax_macd.bar(recent_data.index, recent_data['MACD'], label='MACD', color='green', alpha=0.5)
                # 标记指定天数内的金叉和死叉
                golden_cross_data = recent_data[recent_data['macd_golden_cross']]
                death_cross_data = recent_data[recent_data['macd_death_cross']]
                if not golden_cross_data.empty:
                    ax_macd.scatter(golden_cross_data.index, golden_cross_data['DIF'], marker='^', color='g', s=100, label='MACD Golden Cross')
                if not death_cross_data.empty:
                    ax_macd.scatter(death_cross_data.index, death_cross_data['DIF'], marker='v', color='r', s=100, label='MACD Death Cross')
                ax_macd.legend()
            for widget in root.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        days_menu.add_command(label=f"{days}天", command=view_stocks_by_days)
    def run_backtest():
        from 回测模块 import backtest
        backtest_results = backtest(stock_data_dict)
        # 创建一个新的窗口用于展示回测结果的文本信息
        result_text_window = tk.Tk()
        result_text_window.title("回测结果文本信息")
        # 创建一个文本框用于显示回测结果
        result_text = tk.Text(result_text_window)
        result_text.pack()
        # 向文本框中插入回测结果信息
        for code, result in backtest_results.items():
            result_text.insert(tk.END, f"股票代码: {code}\n")
            result_text.insert(tk.END, f"初始资金: 100000\n")
            result_text.insert(tk.END, f"最终资金: {result['final_capital']:.2f}\n")
            result_text.insert(tk.END, f"总收益率: {result['final_return'] * 100:.2f}%\n")
            result_text.insert(tk.END, f"夏普比率: {result['sharpe_ratio']:.2f}\n")
            result_text.insert(tk.END, f"最大回撤: {result['max_drawdown'] * 100:.2f}%\n")
            result_text.insert(tk.END, "交易记录:\n")
            for trade in result['trades']:
                result_text.insert(tk.END, f"{trade[0]} at {trade[1]} with price {trade[2]:.2f}\n")
            result_text.insert(tk.END, "持仓数量变化记录:\n")
            for change in result['position_changes']:
                result_text.insert(tk.END, f"{change[0]}: {change[1]}\n")  # 显示持仓数量变化信息
            result_text.insert(tk.END, "\n")
    def run_backtest_plot():
        from 回测模块 import backtest
        backtest_results = backtest(stock_data_dict)
        # 创建一个新的窗口用于展示所有回测结果的图
        result_window = tk.Toplevel()  # 使用 Toplevel 而不是 Tk 来创建新窗口
        result_window.title("回测结果图")
        for code, result in backtest_results.items():
            # 创建 GridSpec 布局
            fig = plt.figure(figsize=(12, 12))
            gs = GridSpec(3, 1, height_ratios=[1, 1, 1])
            # 绘制买点分布
            ax1 = fig.add_subplot(gs[0])
            result['buy_distribution'].plot(kind='bar', ax=ax1)
            # 设置标题和标签的字体大小
            ax1.set_title(f'{code} 买点分布', fontsize=16)
            ax1.set_xlabel('价格区间', fontsize=12)
            ax1.set_ylabel('买点数量', fontsize=12)
            # 旋转 x 轴标签，避免重叠
            plt.xticks(rotation=45)
            # 绘制买卖频谱
            ax2 = fig.add_subplot(gs[1])
            result['buy_counts'].plot(kind='line', ax=ax2, label='买入次数')
            result['sell_counts'].plot(kind='line', ax=ax2, label='卖出次数')
            ax2.set_title(f'{code} 买卖频谱')
            ax2.set_xlabel('时间（月）')
            ax2.set_ylabel('买卖次数')
            ax2.legend()
            # 绘制资产变化趋势图
            ax3 = fig.add_subplot(gs[2])
            ax3.plot(result['capital_history'], color='blue', linewidth=2, linestyle='-', marker='o', markersize=5)
            ax3.set_facecolor('#f0f0f0')  # 设置背景颜色
            ax3.grid(True, linestyle='--', alpha=0.7)  # 添加网格线
            ax3.set_title(f'{code} 资产变化趋势')
            ax3.set_xlabel('时间')
            ax3.set_ylabel('资产价值')
            # 调整子图间距
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=result_window)
            canvas.draw()
            canvas.get_tk_widget().pack()
        result_window.mainloop()
    view_menu.add_command(label="运行回测（生成结果）", command=run_backtest)
    view_menu.add_command(label="运行回测（生成结果图）", command=run_backtest_plot)
    def show_prediction_results():
        predictions = predict_stock_prices(stock_data_dict, future_days=20)
        result_window = tk.Toplevel(root)
        result_window.title("股票预测结果")
        text = tk.Text(result_window)
        text.pack()
        for code, prediction_df in predictions.items():
            text.insert(tk.END, f"股票代码: {code}\n")
            for _, row in prediction_df.iterrows():
                date = row['Date'].strftime('%Y-%m-%d')
                price = row['Predicted_Close']
                text.insert(tk.END, f"日期: {date}, 预测收盘价: {price:.2f}\n")
            text.insert(tk.END, "\n")
    view_menu.add_command(label="查看所有股票", command=view_all_stocks)
    view_menu.add_command(label="查看股票预测结果", command=show_prediction_results)
    root.config(menu=menubar)
    # 初始显示全部股票
    view_all_stocks()
    root.mainloop()