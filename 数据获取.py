import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import random


def fetch_stock_data():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/521.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
    ]
    headers = {'User-Agent': random.choice(user_agents)}
    url = 'http://example.com/stock_data'  # 替换为实际的股票数据网址
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果请求不成功，将引发 HTTPError
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_rows = soup.find_all('tr')
        for row in stock_rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                stock_info = {
                    'name': columns[0].text,
                    'code': columns[1].text,
                    'price': float(columns[2].text)
                }
                collection.insert_one(stock_info)
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except ValueError as e:
        print(f"数据解析错误: {e}")


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_data']
    collection = db['stock_info']
    fetch_stock_data()