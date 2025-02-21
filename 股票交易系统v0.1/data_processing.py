import pandas as pd
def get_recent_data(data, days):
    """
    获取最近指定天数的数据
    :param data: 原始数据
    :param days: 指定的天数
    :return: 最近指定天数的数据
    """
    return data.iloc[-days:]
def get_golden_cross_data(data):
    """
    获取金叉数据
    :param data: 原始数据
    :return: 金叉数据
    """
    return data[data['macd_golden_cross']]
def get_death_cross_data(data):
    """
    获取死叉数据
    :param data: 原始数据
    :return: 死叉数据
    """
    return data[data['macd_death_cross']]