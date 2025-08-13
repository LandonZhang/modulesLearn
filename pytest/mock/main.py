import requests


def get_weather(city):
    response = requests.get(
        f"https://api.weathen.com/v1/{city}"
    )  # 返回的是 mock.return_value
    if response.status_code == 200:
        return response.json()  # 发起函数调用，再返回一个 mock 对象
    else:
        raise ValueError("Could not fetch weather data")
