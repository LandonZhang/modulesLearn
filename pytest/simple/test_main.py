# 文件一定要命名为 test_{需要测试的文件名}
# 对于单个文件手动制定测试就没有影响，但是如果要大批量测试，就会导致 pytest 找不到文件
import pytest
from main import add, divide
import main


def test_add():
    assert add(1, 2) == 3, "1 + 2 should be 3"


# 测试预期行为内的报错
def test_divide():
    # 按照报错类型和报错提示锁定报错(提示不用完全一样，有部分词命中即可)
    with pytest.raises(ValueError, match="The second param can't be 0"):
        divide(1, 0)
    assert divide(4, 2) == 2, "4 + 2 should be 2"


# 初识命名空间
for key, value in main.__dict__.items():
    print(f"键:{key}, 值:{value}")

"""
从返回值可以看到 main.__dict__ 中会将引入的模块名作为键，实际内存位置作为值。
调用 requests 模块无非就是从对应内存位置拿到其中方法
如果有种办法能对这个命名空间中 requests 对应的内存位置进行修改，
我们还能正确调用 requests 库吗？ -> 不能，但这正是给我们模拟请求时伪造假请求提供了通道
"""
