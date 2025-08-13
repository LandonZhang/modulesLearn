| 选项                 |                    作用                    |
| -------------------- | :-----------------------------------------: |
| `-v`/`--verbose` |    详细输出，每个测试函数的状态都会显示    |
| `-q`/`--quiet`   |   简洁输出，只显示总体结果，减少冗余信息   |
| `-k "关键字"`      |   只运行函数名或类名包含指定关键字的测试   |
| `-m "marker"`      |   只运行被指定 `@pytest.mark`标记的测试   |
| `--tb=short`       | long 显示详细的 traceback. short 显示简洁的 |

---

### 使用 @pytest.mark. 标记特定测试用例

1. 给测试函数加标记
   用 @pytest.mark.标记名 装饰器，例如：

```python
import pytest
@pytest.mark.slow
def test_long_computation():
    assert 2 + 2 == 4

@pytest.mark.database
def test_database_connection():
    assert True
```


2. 运行特定标记的测试
使用 -m 选项：

```bash
pytest -m slow         # 只运行标记为 slow 的测试
pytest -m "slow or database"  # slow 或 database 标记的测试都运行
pytest -m "not slow"   # 排除 slow 标记的测试
```
