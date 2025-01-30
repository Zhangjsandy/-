# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('438682642c64d7140154f9f9bf4c05c0bbef7246d0209b035a8ecf28')
# 拉取数据
df = pro.stock_basic(**{
    "ts_code": "600519.SH",
    "name": "\u8d35\u5dde\u8305\u53f0",
    "exchange": "SSE",
    "market": "",
    "is_hs": "H",
    "list_status": "L",
    "limit": 10000000000000,
    "offset": 0
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "cnspell",
    "market",
    "list_date",
    "act_name",
    "act_ent_type"
])
print(df)
