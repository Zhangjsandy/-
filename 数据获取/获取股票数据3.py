import requests
import re
import json
import pandas as pd
from pymongo import MongoClient
def get_one_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    # 发送请求
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # 正则解析返回的源码数据，创建一个字典储存
        json_data_match = re.search(r'\((.*)\)', response.text)
        if json_data_match:
            # 提取 JSON 数据部分
            json_data = json_data_match.group(1)
            try:
                # 解析 JSON
                data_dict = json.loads(json_data)
                # 提取需要的字段
                if 'data' in data_dict and 'diff' in data_dict['data']:
                    extracted_data = data_dict['data']['diff']
                    # 用于存储数据
                    data_list = []
                    for entry in extracted_data:
                        data_list.append({
                            "代码": entry.get("f12"),
                            "名称": entry.get("f14"),
                            "最新价": float(entry.get("f2", 0)),
                            "单日涨跌幅": float(entry.get("f3", 0)),
                            "按日主力净流入净额": float(entry.get("f62", 0)),
                            "单日主力净流入净占比": float(entry.get("f184", 0)),
                            "单日超大单净流入净额": float(entry.get("f66", 0)),
                            "单日超大单净流入净占比": float(entry.get("f69", 0)),
                            "单日大单净流入净额": float(entry.get("f72", 0)),
                            "单日大单净流入净占比": float(entry.get("f75", 0)),
                            "单日中单净流入净额": float(entry.get("f78", 0)),
                            "单日中单净流入净占比": float(entry.get("f81", 0)),
                            "单日小单净流入净额": float(entry.get("f84", 0)),
                            "单日小单净流入净占比": float(entry.get("f87", 0))
                        })
                    return data_list
            except json.JSONDecodeError:
                print("Error decoding JSON.")
    return None
def save_to_mongodb(data, collection):
    try:
        collection.insert_many(data)
        print("数据已成功保存到 MongoDB。")
    except Exception as e:
        print(f"保存数据到 MongoDB 时出错: {e}")
def fetch_and_save_one_page(base_url, page, collection):
    # 替换页码参数 pn
    page_url = base_url.replace("pn=1", f"pn={page}")
    print(f"Fetching page {page}...")
    result = get_one_data(page_url)
    if result:
        # 保存数据到 MongoDB 数据库
        save_to_mongodb(result, collection)
    else:
        print(f"Failed to retrieve data for page {page}.")
if __name__ == '__main__':
    url = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112306315871240374897_1737296715841&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
    # 连接 MongoDB 数据库
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_db']  # 数据库名称
    collection = db['stock_collection']  # 集合名称
    # 用户输入总页数
    total_pages = int(input("请输入要抓取的总页数："))
    # 每页抓取并保存
    for page in range(1, total_pages + 1):
        fetch_and_save_one_page(url, page, collection)