from pymongo import MongoClient
def query_multiple_stock_data():
    # 连接到本地 MongoDB 服务器，默认端口是 27017
    client = MongoClient('mongodb://localhost:27017/')
    # 访问数据库，如果数据库不存在，MongoDB 会在你第一次插入数据时自动创建它
    db = client['stock_data']
    # 获取集合，如果集合不存在，MongoDB 会在你第一次插入数据时自动创建它
    collection = db['stock_info']
    # 查询所有数据
    all_stocks = collection.find()
    print("所有股票数据:")
    for stock in all_stocks:
        print(stock)
    # 查询价格在 0 到 200 之间的股票
    range_price_stocks = collection.find({'price': {'$gte': 0, '$lte': 200}})
    print("\n价格在 0 到 200 之间的股票:")
    for stock in range_price_stocks:
        print(stock)
if __name__ == "__main__":
    query_multiple_stock_data()