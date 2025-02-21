import matplotlib.pyplot as plt
from plotting import plot_stock_data, embed_plot
from data_processing import get_recent_data
def view_all_stocks(root, stock_data_dict):
    num_stocks = len(stock_data_dict)
    fig, axes = plt.subplots(num_stocks, ncols=3, figsize=(18, 6 * num_stocks), gridspec_kw={'width_ratios': [3, 1, 1]})
    for i, (code, data) in enumerate(stock_data_dict.items()):
        if num_stocks == 1:
            ax1 = axes[0]
            ax2 = axes[1]
            ax_macd = axes[2]
        else:
            ax1 = axes[i, 0]
            ax2 = axes[i, 1]
            ax_macd = axes[i, 2]
        plot_stock_data(data, ax1, ax2, ax_macd, code)
    embed_plot(fig, root)
def view_single_stock(root, stock_data_dict, code):
    data = stock_data_dict[code]
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), gridspec_kw={'width_ratios': [3, 1, 1]})
    ax1 = axes[0]
    ax2 = axes[1]
    ax_macd = axes[2]
    plot_stock_data(data, ax1, ax2, ax_macd, code)
    embed_plot(fig, root)
def view_stocks_by_days(root, stock_data_dict, days):
    num_stocks = len(stock_data_dict)
    fig, axes = plt.subplots(num_stocks, ncols=3, figsize=(18, 6 * num_stocks), gridspec_kw={'width_ratios': [3, 1, 1]})
    for i, (code, data) in enumerate(stock_data_dict.items()):
        recent_data = get_recent_data(data, days)
        if num_stocks == 1:
            ax1 = axes[0]
            ax2 = axes[1]
            ax_macd = axes[2]
        else:
            ax1 = axes[i, 0]
            ax2 = axes[i, 1]
            ax_macd = axes[i, 2]
        plot_stock_data(recent_data, ax1, ax2, ax_macd, f"{code} ({days}天)")
    embed_plot(fig, root)