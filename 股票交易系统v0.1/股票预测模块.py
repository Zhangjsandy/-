import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
def predict_stock_prices(stock_data_dict, future_days=20):
    """
    使用随机森林模型预测股票未来指定天数的收盘价
    :param stock_data_dict: 包含股票数据的字典，键为股票代码，值为DataFrame
    :param future_days: 预测的未来天数，默认为20天
    :return: 预测结果的字典，键为股票代码，值为包含日期和预测价格的DataFrame
    """
    predictions = {}
    for code, data in stock_data_dict.items():
        # 提取特征和标签
        features = data[['Open', 'High', 'Low', 'Volume']]
        labels = data['Close']
        # 创建随机森林回归模型
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        # 训练模型
        model.fit(features, labels)
        # 获取最后一天的日期
        last_date = data.index[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days)
        # 构建未来 20 天的特征数据（这里简单假设特征值保持最后一天的值）
        last_features = features.iloc[-1].values
        future_features = np.tile(last_features, (future_days, 1))
        # 进行预测
        y_pred = model.predict(future_features)
        # 创建包含日期和预测价格的DataFrame
        prediction_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Close': y_pred
        })
        predictions[code] = prediction_df
    return predictions