#发送请求：模拟浏览器对于url发送请求
#导入数据请求模块
import requests
#导入数据解析模块
import json
import re
def get_one_data(url):
    # User-Agent:用户代理：浏览器基本身份信息
    headers = {
        'User-Agent'
        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }  #字典形式：构建完整的键值对
    # 发送请求
    response = requests.get(url=url, headers=headers)
    print("Status Code:", response.status_code)  # 检查状态码
    if response.status_code == 200:
        json_data_match = re.search(r'\((.*)\)', response.text)
        if json_data_match:
            json_data = json_data_match.group(1)
            try:
                data_dict = json.loads(json_data)
                if 'data' in data_dict and 'diff' in data_dict['data']:
                    extracted_data = data_dict['data']['diff']
                    data_list = []
                    for entry in extracted_data:
                        data_list.append({
                            "代码": entry.get("SECURITY_CODE"),
                            "名称": entry.get("SECURITY_NAME"),
                            "最新价": float(entry.get("NEWEST_PRICE", 0)),
                            "发行总数": float(entry.get("ISSUE_NUM", 0)),
                            "网上发行": float(entry.get("ONLINE_ISSUE_NUM", 0)),
                            "顶格申购需配市值(万元)": float(entry.get("TOP_APPLY_MARKETCAP", 0)),
                            "申购上限": float(entry.get("ONLINE_APPLY_UPPER", 0)),
                            "首日收盘价": float(entry.get("CLOSE_PRICE", 0)),
                            "发行市盈率": float(entry.get("AFTER_ISSUE_PE", 0)),
                            "行业市盈率": float(entry.get("INDUSTRY_PE_NEW", 0)),
                            "中签率": float(entry.get("ONLINE_ISSUE_LWR", 0)),
                            "询价累计报价倍数": float(entry.get("INITIAL_MULTIPLE", 0)),
                            "配售对象累计报价家数": float(entry.get("OFFLINE_EP_OBJECT", 0)),
                            "涨幅(%)": float(entry.get("TOTAL_CHANGE", 0)),
                            "每中一签获利":float(entry.get("PROFIT", 0))
                        })
                    return data_list
            except json.JSONDecodeError:
                print("Error decoding JSON.")
    return None
if __name__ == '__main__':
    #url地址
    url=('https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308992725888560138_1737036849536&sortColumns=APPLY_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=2&reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE%2CSECURITY_NAME%2CTRADE_MARKET_CODE%2CAPPLY_CODE%2CTRADE_MARKET%2CMARKET_TYPE%2CORG_TYPE%2CISSUE_NUM%2CONLINE_ISSUE_NUM%2COFFLINE_PLACING_NUM%2CTOP_APPLY_MARKETCAP%2CPREDICT_ONFUND_UPPER%2CONLINE_APPLY_UPPER%2CPREDICT_ONAPPLY_UPPER%2CISSUE_PRICE%2CLATELY_PRICE%2CCLOSE_PRICE%2CAPPLY_DATE%2CBALLOT_NUM_DATE%2CBALLOT_PAY_DATE%2CLISTING_DATE%2CAFTER_ISSUE_PE%2CONLINE_ISSUE_LWR%2CINITIAL_MULTIPLE%2CINDUSTRY_PE_NEW%2COFFLINE_EP_OBJECT%2CCONTINUOUS_1WORD_NUM%2CTOTAL_CHANGE%2CPROFIT%2CLIMIT_UP_PRICE%2CINFO_CODE%2COPEN_PRICE%2CLD_OPEN_PREMIUM%2CLD_CLOSE_CHANGE%2CTURNOVERRATE%2CLD_HIGH_CHANG%2CLD_AVERAGE_PRICE%2COPEN_DATE%2COPEN_AVERAGE_PRICE%2CPREDICT_PE%2CPREDICT_ISSUE_PRICE2%2CPREDICT_ISSUE_PRICE%2CPREDICT_ISSUE_PRICE1%2CPREDICT_ISSUE_PE%2CPREDICT_PE_THREE%2CONLINE_APPLY_PRICE%2CMAIN_BUSINESS%2CPAGE_PREDICT_PRICE1%2CPAGE_PREDICT_PRICE2%2CPAGE_PREDICT_PRICE3%2CPAGE_PREDICT_PE1%2CPAGE_PREDICT_PE2%2CPAGE_PREDICT_PE3%2CSELECT_LISTING_DATE%2CIS_BEIJING%2CINDUSTRY_PE_RATIO%2CINDUSTRY_PE%2CIS_REGISTRATION&quoteColumns=f2~01~SECURITY_CODE~NEWEST_PRICE&quoteType=0&filter=(APPLY_DATE%3E%272010-01-01%27)&source=WEB&client=WEB')
    result = get_one_data(url)
    if result:
        print(result)
    else:
        print("Failed to retrieve or parse data.")
