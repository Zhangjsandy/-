from pymongo import MongoClient
def insert_multiple_stock_data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_data']
    collection = db['stock_info']
    new_stocks = [
        {'name': '东方财富', 'code': '300059', 'price': 23.86},
        {'name': '同花顺', 'code': '300033', 'price': 290.00},
        {'name': '赛力斯', 'code': '601127', 'price': 138.71},
        {'name': '卧龙电驱', 'code': '600580', 'price': 18.87},
        {'name': '兆易创新', 'code': '603986', 'price': 129.64}
    ]
    # 插入多条数据
    result = collection.insert_many(new_stocks)
    print(f"插入数据的 IDs: {result.inserted_ids}")
if __name__ == "__main__":
    insert_multiple_stock_data()