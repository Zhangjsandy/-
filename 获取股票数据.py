#发送请求：模拟浏览器对于url发送请求
#导入数据请求模块
import requests
#导入数据解析模块
import re
import json
def get_one_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }#字典形式：构建完整的键值对
    #发送请求
    response = requests.get(url=url,headers=headers)
    print("Status Code:", response.status_code)  #检查状态码
    if response.status_code == 200:
        data_str = response.text
        print("Raw Data:", data_str[:1000])  #只打印前500个字符进行检查
        # 移除可能的回调函数，提取JSON数据部分
        json_data_match = re.search(r'\((.*)\)', data_str)
        if json_data_match:
            # 提取JSON数据部分
            json_data = json_data_match.group(1)
            try:
                #解析JSON
                data_dict = json.loads(json_data)
                #打印解析后的JSON数据，便于调试
                print("Parsed JSON:", data_dict)
                #继续提取需要的字段
                pattern = re.compile(
                    r'"f12":"(.*?)".*?"f14":"(.*?)".*?"f2":(.*?),.*?"f172":(.*?),.*?"f267":(.*?),'
                    r'.*?"f268":(.*?),.*?"f269":(.*?),.*?"f270":(.*?),.*?"f271":(.*?),'
                    r'.*?"f272":(.*?),.*?"f273":(.*?),.*?"f274":(.*?),.*?"f275":(.*?),.*?"f276":(.*?)'
                )
                #用于存储提取的数据
                data = []
                for match in pattern.finditer(json_data):
                    data.append({
                        "f12": match.group(1),
                        "f14": match.group(2),
                        "f2": float(match.group(3)),
                        "f3": float(match.group(4)),
                        "f62": float(match.group(5)),
                        "f184": float(match.group(6)),
                        "f66": float(match.group(7)),
                        "f69": float(match.group(8)),
                        "f72": float(match.group(9)),
                        "f75": float(match.group(10)),
                        "f78": float(match.group(11)),
                        "f81": float(match.group(12)),
                        "f84": float(match.group(13)),
                        "f87": float(match.group(14)),
                    })
                return data
            except json.JSONDecodeError:
                print("Error decoding JSON.")
                return None
    return None
if __name__ == '__main__':
    url = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112306315871240374897_1737296715841&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
    result = get_one_data(url)
    if result:
        for entry in result:
            print(entry)
    else:
        print("Failed to retrieve or parse data.")

