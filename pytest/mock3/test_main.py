import pytest
from main import UserService, APIClient


def test_get_username_with_mock(mocker):
    # 直接指定创建一个 mock 对象，不等任何调用
    # 并且这个 mock 记录了类中的方法和属性，不允许定义没有的函数和属性
    mock_api_client = mocker.Mock(spec=APIClient)

    # 可以直接对对象的方法进行操作，不用再 mock_api_client.return_value 了
    mock_api_client.get_user_data.return_value = {"id": 1, "name": "Alice"}
    service = UserService(mock_api_client)
    result = service.get_username(1)  # 触发并返回 get_user_data.return_value 定义的值

    assert result == "ALICE"
    mock_api_client.get_user_data.assert_called_once_with(1)  # 确保正确调用
