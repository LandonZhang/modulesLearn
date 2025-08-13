import pytest
from main import is_prime


# 如果我们希望传入很多值进行批量测试，可以使用 parametrize 自动传入多个值进行测试
# 第一个字符串制定参数的名称，第二个参数使用元组列表表示多个对应值
# 注意函数的输入参数名要保持一致
@pytest.mark.parametrize("num, expected", [(1, False), (2, True), (3, True), (7, True)])
def test_is_prime(num, expected):
    assert is_prime(num) == expected
