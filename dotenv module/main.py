from dotenv import load_dotenv
import os

# 将环境文件中的信息加载进入代码作用域中
load_dotenv("myenv.env")

# 通过 os 库进行环境信息加载
api_key = os.getenv("APIKEY")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

print(api_key, username, password)
