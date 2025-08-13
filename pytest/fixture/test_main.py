import pytest
from main import UserManager


# fixture 可以定义每个测试函数之前要执行的操作:
# 创建一个示例对象，创建一个数据库连接等...
@pytest.fixture
def user_manager():
    """Creates a fresh instance of UserManager before each test."""
    return UserManager()


# user_manager 的名称一定要保持一致
# 将自动调用 user_manager 函数，并将返回值存储进入 user_manager 变量中
def test_add_user(user_manager):
    assert user_manager.add_user("john_doe", "john@example.com") == True  # noqa: E712
    assert user_manager.get_user("john_doe") == "john@example.com"


def test_add_duplicate_user(user_manager):
    user_manager.add_user("john_doe", "john@example.com")
    with pytest.raises(ValueError):
        user_manager.add_user("john_doe", "another@example.com")
