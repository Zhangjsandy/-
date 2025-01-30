import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
def fetch_eastmoney_stock_data():
    url = 'http://quote.eastmoney.com/stock_list.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_list = []
        li_elements = soup.find_all('li')
        for li in li_elements:
            a_tag = li.find('a')
            if a_tag:
                href = a_tag.get('href')
                text = a_tag.get_text()
                if href and text:
                    code = href.split('/')[-1].split('.')[0]
                    name = text
                    # 尝试提取价格
                    price_element = a_tag.find('span', class_='price')
                    price = float(price_element.text) if price_element else 0.0
                    stock_list.append({'code': code, 'name': name, 'price': price})
        client = MongoClient('mongodb://localhost:27017/')
        db = client['stock_data']
        collection = db['eastmoney_stocks']
        collection.insert_many(stock_list)
        print("股票数据已插入 MongoDB")
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except AttributeError as e:
        print(f"解析元素失败: {e}")
    except Exception as e:
        print(f"其他错误: {e}")
if __name__ == "__main__":
    fetch_eastmoney_stock_data()