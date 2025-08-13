import sqlite3


def save_user(name, age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()  # 测试中这里是一个 mock 对象，所以什么方法都可以用
    cursor.execute("INSERT INTO users (name,age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
