import numpy as np
import pandas as pd
def backtest(stock_data_dict, initial_capital=100000):
    backtest_results = {}
    for code, data in stock_data_dict.items():
        capital = initial_capital
        position = 0
        trades = []
        capital_history = []  # 记录每日的资产价值
        position_changes = []  # 记录持仓数量变化
        buy_prices = []  # 记录买点价格
        buy_dates = []  # 记录买点日期
        sell_dates = []  # 记录卖点日期
        for i in range(1, len(data)):
            if data['macd_golden_cross'].iloc[i] and position == 0:
                # 金叉买入
                position = capital / data['Close'].iloc[i]
                capital = 0
                trades.append(('Buy', data.index[i], data['Close'].iloc[i]))
                position_changes.append((data.index[i], position))
                buy_prices.append(data['Close'].iloc[i])
                buy_dates.append(data.index[i])
            elif data['macd_death_cross'].iloc[i] and position > 0:
                # 死叉卖出
                capital = position * data['Close'].iloc[i]
                position = 0
                trades.append(('Sell', data.index[i], data['Close'].iloc[i]))
                position_changes.append((data.index[i], position))
                sell_dates.append(data.index[i])
            # 记录每日的资产价值
            if position > 0:
                daily_value = position * data['Close'].iloc[i]
            else:
                daily_value = capital
            capital_history.append(daily_value)
        # 最后一天如果还有持仓，按收盘价卖出
        if position > 0:
            capital = position * data['Close'].iloc[-1]
            trades.append(('Sell', data.index[-1], data['Close'].iloc[-1]))
            position_changes.append((data.index[-1], 0))
            capital_history.append(capital)
            sell_dates.append(data.index[-1])
        # 计算收益率
        returns = np.array(capital_history) / initial_capital - 1
        # 计算夏普比率
        daily_returns = np.diff(capital_history) / np.array(capital_history[:-1])
        sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
        # 计算最大回撤
        max_drawdown = (np.maximum.accumulate(capital_history) - capital_history) / np.maximum.accumulate(capital_history)
        max_drawdown = np.max(max_drawdown)
        final_return = (capital - initial_capital) / initial_capital
        # 统计买点分布
        if buy_prices:
            bins = np.linspace(min(buy_prices), max(buy_prices), 10)
            buy_distribution = pd.cut(buy_prices, bins).value_counts()
        else:
            buy_distribution = pd.Series()
        # 统计买卖频谱
        buy_counts = pd.Series(buy_dates).dt.to_period('M').value_counts().sort_index()
        sell_counts = pd.Series(sell_dates).dt.to_period('M').value_counts().sort_index()
        backtest_results[code] = {
            'final_capital': capital,
            'final_return': final_return,
            'trades': trades,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'position_changes': position_changes,
            'capital_history': capital_history,
            'buy_distribution': buy_distribution,
            'buy_counts': buy_counts,
            'sell_counts': sell_counts
        }
    return backtest_results