import requests
from requests import get


def add(a, b):
    print("正在计算两数之和")
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("The second param can't be 0")
    else:
        return a / b


print(f"main 文件的命名空间是：")
