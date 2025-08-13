import pytest
from main import get_weather

# 有时候我们的代码是向外发出请求的，但是外部的失败不在我们的控制范围内
# 所以我们可以使用 mock 数据来模型外部正确响应，确保自己没问题
# 它的本质就是我们在 simple/ 中谈到的修改命名空间，将引用指向一个 mock 对象


def test_get_weather(mocker):
    # 修改 main.__dict__["requests"].__dict__["get"] 指向的东西
    mock_get = mocker.patch("main.requests.get")
    # 对于 mock 对象，其拥有的属性和函数十分自由，你每访问一个新的函数或属性就新创建一个 mocker 来储存你写入的信息
    # 调用 mock 对象默认返回: mock.return_value 如果没有设定值就返回一个 mock
    # 调用 mock.attr 默认调用 __getattr__ 返回值 如果没有也返回一个 mock
    """
    当 get 被替换后，每次调用 get 都调用的是 mocker 对象，自动返回 return_value  
    故想设置值一定要从 return_value 中设置 
    """
    # 手动设置参数对应值
    mock_get.return_value.status_code = 200
    # mock_get.return_value.status_code = 210  # 由于状态码不对，会报错

    # mock_get 原始，return_value 返回，json 函数调用再次创建
    # 这一句代码创建了 3 个 mock
    # 设置 .json() 调用后的返回值
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}

    result = get_weather("Dubai")
    # requests.get().json() 之后返回的结果
    assert result == {"temperature": 25, "condition": "Sunny"}
    # mocker 会记住自己是否被调用以及调用次数等信息
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")
