from main import save_user


# 也可以 patch 数据库连接
def test_save_user(mocker):
    mock_conn = mocker.patch("main.sqlite3.connect")
    save_user("Alice", 30)
    mock_conn.assert_called_once_with("users.db")

    # mock 的方法和属性也可以在正式文件中通过调用而定义，使用下面方式拿到新生成的 mock
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name,age) VALUES (?, ?)", ("Alice", 30)
    )
