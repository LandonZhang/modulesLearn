# pytest 模块完整教程

## 目录

1. [pytest 简介](#pytest-简介)
2. [基础测试](#基础测试)
3. [命令行选项](#命令行选项)
4. [异常测试](#异常测试)
5. [Fixture 使用](#fixture-使用)
6. [参数化测试](#参数化测试)
7. [Mock 测试](#mock-测试)
8. [高级 Mock 技巧](#高级mock技巧)
9. [最佳实践](#最佳实践)

## pytest 简介

pytest 是 Python 中最流行的测试框架之一，具有简洁的语法和强大的功能。它支持简单的单元测试到复杂的功能测试。

### 安装

```bash
pip install pytest
```

## 基础测试

### 文件命名规范

测试文件必须遵循命名规范，否则 pytest 无法自动发现：
- 测试文件：`test_*.py` 或 `*_test.py`
- 测试函数：以 `test_` 开头
- 测试类：以 `Test` 开头

### 基础示例

```python
# main.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b
```

```python
# test_main.py
from main import add, divide

def test_add():
    assert add(1, 2) == 3, "1 + 2 应该等于 3"

def test_divide():
    assert divide(4, 2) == 2, "4 / 2 应该等于 2"
```

## 命令行选项

| 选项 | 作用 |
|------|------|
| `-v/--verbose` | 详细输出，显示每个测试函数的状态 |
| `-q/--quiet` | 简洁输出，只显示总体结果 |
| `-k "关键字"` | 只运行函数名包含指定关键字的测试 |
| `-m "marker"` | 只运行被指定标记的测试 |
| `--tb=short` | 显示简洁的错误追踪信息 |
| `--tb=long` | 显示详细的错误追踪信息 |

### 使用标记 (Markers)

```python
import pytest

@pytest.mark.slow
def test_long_computation():
    # 耗时较长的测试
    assert 2 + 2 == 4

@pytest.mark.database
def test_database_connection():
    # 数据库相关测试
    assert True
```

```bash
# 运行特定标记的测试
pytest -m slow                    # 只运行 slow 标记的测试
pytest -m "slow or database"      # 运行 slow 或 database 标记的测试
pytest -m "not slow"              # 排除 slow 标记的测试
```

## 异常测试

使用 `pytest.raises()` 测试期望的异常：

```python
import pytest

def test_divide_by_zero():
    # 测试除零异常
    with pytest.raises(ValueError, match="除数不能为0"):
        divide(1, 0)
```

## Fixture 使用

Fixture 用于在测试前准备测试环境，在测试后清理资源。

### 基础 Fixture

```python
# main.py
class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, email):
        if username in self.users:
            raise ValueError("用户已存在")
        self.users[username] = email
        return True
    
    def get_user(self, username):
        return self.users.get(username)
```

```python
# test_main.py
import pytest
from main import UserManager

@pytest.fixture
def user_manager():
    """每个测试前创建一个新的 UserManager 实例"""
    return UserManager()

def test_add_user(user_manager):
    assert user_manager.add_user("john", "john@example.com") == True
    assert user_manager.get_user("john") == "john@example.com"

def test_add_duplicate_user(user_manager):
    user_manager.add_user("john", "john@example.com")
    with pytest.raises(ValueError, match="用户已存在"):
        user_manager.add_user("john", "another@example.com")
```

### 带清理的 Fixture (yield)

```python
# main.py
class Database:
    def __init__(self):
        self.data = {}
    
    def add_user(self, user_id, name):
        if user_id in self.data:
            raise ValueError("用户已存在")
        self.data[user_id] = name
    
    def get_user(self, user_id):
        return self.data.get(user_id, None)
    
    def delete_user(self, user_id):
        if user_id in self.data:
            del self.data[user_id]
```

```python
# test_main.py
import pytest
from main import Database

@pytest.fixture
def db():
    """提供数据库实例并在测试后清理"""
    database = Database()
    yield database  # 在这里停止，执行测试
    database.data.clear()  # 测试完成后清理数据

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"

def test_delete_user(db):
    db.add_user(2, "Bob")
    db.delete_user(2)
    assert db.get_user(2) is None
```

## 参数化测试

使用 `@pytest.mark.parametrize` 进行批量测试：

```python
# main.py
from math import floor

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, floor(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

```python
# test_main.py
import pytest
from main import is_prime

@pytest.mark.parametrize("num, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (7, True),
    (9, False)
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected
```

## Mock 测试

Mock 用于模拟外部依赖，如 API 调用、数据库连接等。

### 基础 Mock 使用

```python
# main.py
import requests

def get_weather(city):
    response = requests.get(f"https://api.weather.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("无法获取天气数据")
```

```python
# test_main.py
import pytest
from main import get_weather

def test_get_weather(mocker):
    # Mock requests.get 方法
    mock_get = mocker.patch("main.requests.get")
    
    # 设置 mock 返回值
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "temperature": 25, 
        "condition": "晴天"
    }
    
    result = get_weather("北京")
    
    # 验证结果
    assert result == {"temperature": 25, "condition": "晴天"}
    # 验证调用
    mock_get.assert_called_once_with("https://api.weather.com/v1/北京")
```

### Mock 数据库操作

```python
# main.py
import sqlite3

def save_user(name, age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
```

```python
# test_main.py
from main import save_user

def test_save_user(mocker):
    # Mock 数据库连接
    mock_conn = mocker.patch("main.sqlite3.connect")
    
    save_user("Alice", 30)
    
    # 验证连接调用
    mock_conn.assert_called_once_with("users.db")
    
    # 获取 cursor mock 对象
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUES (?, ?)", 
        ("Alice", 30)
    )
```

## 高级 Mock 技巧

### 使用 spec 参数

使用 `spec` 参数可以限制 mock 对象只能调用原类的方法：

```python
# main.py
import requests

class APIClient:
    def get_user_data(self, user_id):
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        raise ValueError("API 请求失败")

class UserService:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_username(self, user_id):
        user_data = self.api_client.get_user_data(user_id)
        return user_data["name"].upper()
```

```python
# test_main.py
import pytest
from main import UserService, APIClient

def test_get_username_with_mock(mocker):
    # 创建有 spec 限制的 mock 对象
    mock_api_client = mocker.Mock(spec=APIClient)
    
    # 设置方法返回值
    mock_api_client.get_user_data.return_value = {"id": 1, "name": "Alice"}
    
    service = UserService(mock_api_client)
    result = service.get_username(1)
    
    assert result == "ALICE"
    mock_api_client.get_user_data.assert_called_once_with(1)
```

## Mock 工作原理深度解析

### 命名空间修改机制

Mock 的本质是修改 Python 的命名空间。当我们导入模块时，模块的 `__dict__` 会存储所有导入的对象：

```python
# 查看命名空间
import main
for key, value in main.__dict__.items():
    print(f"键: {key}, 值: {value}")

# 输出示例:
# 键: requests, 值: <module 'requests' from '/path/to/requests/__init__.py'>
# 键: get_weather, 值: <function get_weather at 0x...>
```

当使用 `mocker.patch("main.requests.get")` 时：
1. 找到 `main.__dict__["requests"]`
2. 修改其 `__dict__["get"]` 指向一个 Mock 对象
3. 原来的 `requests.get` 被替换为 Mock 对象

### Mock 对象特性

Mock 对象具有以下特性：
- **动态属性创建**：访问不存在的属性会自动创建新的 Mock 对象
- **调用记录**：自动记录所有方法调用及参数
- **返回值设置**：通过 `return_value` 设置调用返回值
- **链式调用支持**：支持 `mock.method().another_method()` 这样的链式调用

```python
def test_mock_behavior():
    from unittest.mock import Mock
    
    mock_obj = Mock()
    
    # 动态创建属性
    result = mock_obj.some_method()  # 返回新的 Mock 对象
    
    # 设置返回值
    mock_obj.get_data.return_value = {"key": "value"}
    assert mock_obj.get_data() == {"key": "value"}
    
    # 验证调用
    mock_obj.get_data.assert_called_once()
```

## 最佳实践

### 1. 测试文件组织

```
project/
├── src/
│   ├── __init__.py
│   ├── models.py
│   └── services.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    └── test_services.py
```

### 2. Fixture 作用域

```python
@pytest.fixture(scope="session")    # 整个测试会话只创建一次
def database_connection():
    pass

@pytest.fixture(scope="module")     # 每个模块创建一次
def test_data():
    pass

@pytest.fixture(scope="function")   # 每个测试函数创建一次（默认）
def user_instance():
    pass
```

### 3. 测试数据管理

```python
# conftest.py
import pytest

@pytest.fixture
def sample_users():
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]

# test_users.py  
def test_user_creation(sample_users):
    user = sample_users[0]
    assert user["name"] == "Alice"
```

### 4. 异常测试模式

```python
def test_comprehensive_error_handling():
    # 测试特定异常
    with pytest.raises(ValueError, match="具体错误信息"):
        problematic_function()
    
    # 测试异常属性
    with pytest.raises(CustomException) as exc_info:
        problematic_function()
    
    assert exc_info.value.error_code == 404
```

### 5. 参数化测试最佳实践

```python
@pytest.mark.parametrize("input_data,expected,description", [
    ({"name": "Alice", "age": 25}, True, "有效用户数据"),
    ({"name": "", "age": 25}, False, "姓名为空"),
    ({"name": "Bob", "age": -1}, False, "年龄为负数"),
], ids=["valid_user", "empty_name", "negative_age"])
def test_user_validation(input_data, expected, description):
    assert validate_user(input_data) == expected
```

### 6. Mock 使用指南

- **只 Mock 你控制不了的部分**：外部 API、文件系统、数据库
- **避免过度 Mock**：不要 Mock 被测试的代码本身
- **使用 spec 参数**：防止调用不存在的方法
- **验证交互**：确保 Mock 对象被正确调用

### 7. 测试命名规范

```python
def test_should_return_user_when_valid_id_provided():
    """测试：当提供有效ID时应该返回用户"""
    pass

def test_should_raise_error_when_user_not_found():
    """测试：当用户不存在时应该抛出错误"""
    pass
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest test_main.py

# 运行特定函数
pytest test_main.py::test_add

# 详细输出
pytest -v

# 显示覆盖率
pytest --cov=src

# 生成HTML覆盖率报告
pytest --cov=src --cov-report=html
```

## 总结

pytest 提供了强大而灵活的测试功能：

1. **简单的断言语法**：直接使用 `assert` 语句
2. **强大的 Fixture 系统**：支持复杂的测试环境准备
3. **参数化测试**：轻松进行批量测试
4. **Mock 支持**：有效隔离外部依赖
5. **丰富的命令行选项**：满足不同测试需求
6. **插件生态**：支持覆盖率、并行测试等扩展功能

通过合理使用这些功能，可以构建可靠、可维护的测试套件，确保代码质量。