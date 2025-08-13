import pytest
from main import Database


@pytest.fixture
def db():
    """Provides a fresh instance of the Database class and cleans up after the test."""
    database = Database()
    yield database  # 调用返回数据库连接，并且运行到这里停止，完全测试完之后将继续执行
    database.data.clear()  # 当使用完数据库的时候，我们总是希望关闭数据库连接以节约资源


def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"


def test_add_duplicate_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="user already exists"):
        db.add_user(1, "Bob")


def test_delete_user(db):
    db.add_user(2, "Bob")
    db.delete_user(2)
    assert db.get_user(2) is None
