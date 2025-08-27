# -*- coding: utf-8 -*-
"""
LRU缓存 (@lru_cache) 教程
========================

学习如何使用LRU缓存来避免重复计算
"""

import time
from functools import lru_cache
import random


def demo_basic_usage():
    """基础使用演示"""
    print("=== 1. 基础使用演示 ===")

    # 无缓存版本
    def slow_calculation(n: int) -> int:
        """模拟慢速计算"""
        print(f"  计算 {n}...")
        time.sleep(0.1)  # 模拟计算时间
        return n * n

    # 有缓存版本
    @lru_cache(maxsize=128)
    def cached_calculation(n: int) -> int:
        """带缓存的计算"""
        print(f"  计算 {n}...")
        time.sleep(0.1)  # 模拟计算时间
        return n * n

    # 测试数据（有重复）
    test_data = [1, 2, 3, 1, 2, 4, 1, 3, 5]

    # 无缓存测试
    print("无缓存版本:")
    start = time.time()
    results1 = [slow_calculation(n) for n in test_data]
    no_cache_time = time.time() - start
    print(f"无缓存耗时: {no_cache_time:.2f}秒")

    # 有缓存测试
    print("\n有缓存版本:")
    start = time.time()
    results2 = [cached_calculation(n) for n in test_data]
    cache_time = time.time() - start
    print(f"有缓存耗时: {cache_time:.2f}秒")
    print(f"性能提升: {no_cache_time / cache_time:.1f}倍")

    # 查看缓存统计
    print(f"缓存统计: {cached_calculation.cache_info()}")


def demo_cache_management():
    """缓存管理演示"""
    print("\n\n=== 2. 缓存管理演示 ===")

    @lru_cache(maxsize=32)
    def fibonacci(n: int) -> int:
        """斐波那契数列（递归+缓存优化）"""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # 计算斐波那契数
    print("计算斐波那契数列:")
    for n in [10, 20, 15, 25, 10]:  # 有重复
        result = fibonacci(n)
        print(f"  fib({n}) = {result}")

    # 显示缓存信息
    cache_info = fibonacci.cache_info()
    print(f"\n缓存统计: {cache_info}")
    print(
        f"命中率: {cache_info.hits / (cache_info.hits + cache_info.misses) * 100:.1f}%"
    )

    # 清理缓存
    print("\n清理缓存...")
    fibonacci.cache_clear()
    print(f"清理后统计: {fibonacci.cache_info()}")


def demo_database_query():
    """数据库查询缓存示例"""
    print("\n\n=== 3. 数据库查询缓存示例 ===")

    # 模拟数据库
    fake_database = {
        1: {"name": "张三", "age": 25, "city": "北京"},
        2: {"name": "李四", "age": 30, "city": "上海"},
        3: {"name": "王五", "age": 28, "city": "广州"},
        4: {"name": "赵六", "age": 32, "city": "深圳"},
        5: {"name": "钱七", "age": 27, "city": "杭州"},
    }

    @lru_cache(maxsize=64)
    def get_user_info(user_id: int) -> dict:
        """获取用户信息（模拟数据库查询）"""
        print(f"  查询数据库: user_id={user_id}")
        time.sleep(0.05)  # 模拟查询延迟
        return fake_database.get(user_id, {"error": "用户不存在"})

    # 模拟用户查询请求（有大量重复）
    user_requests = [1, 2, 1, 3, 2, 1, 4, 2, 5, 1, 3]

    print(f"处理 {len(user_requests)} 个用户查询请求:")
    start = time.time()

    for user_id in user_requests:
        user_info = get_user_info(user_id)
        print(f"  用户{user_id}: {user_info.get('name', 'N/A')}")

    query_time = time.time() - start
    cache_info = get_user_info.cache_info()

    print(f"\n查询完成:")
    print(f"  总耗时: {query_time:.2f}秒")
    print(f"  缓存统计: {cache_info}")
    print(f"  实际数据库查询次数: {cache_info.misses}")
    print(f"  缓存节省的查询次数: {cache_info.hits}")


def demo_complex_parameters():
    """复杂参数缓存演示"""
    print("\n\n=== 4. 复杂参数缓存演示 ===")

    @lru_cache(maxsize=100)
    def complex_calculation(x: float, y: float, operation: str) -> float:
        """复杂计算函数"""
        print(f"  执行计算: {x} {operation} {y}")
        time.sleep(0.02)  # 模拟计算时间

        if operation == "add":
            return x + y
        elif operation == "multiply":
            return x * y
        elif operation == "power":
            return x**y
        else:
            return 0.0

    # 测试不同参数组合（有重复）
    calculations = [
        (2.0, 3.0, "add"),
        (2.0, 3.0, "multiply"),
        (2.0, 3.0, "add"),  # 重复
        (4.0, 5.0, "power"),
        (2.0, 3.0, "multiply"),  # 重复
        (1.5, 2.5, "add"),
        (2.0, 3.0, "power"),
    ]

    print("执行复杂计算:")
    for x, y, op in calculations:
        result = complex_calculation(x, y, op)
        print(f"  结果: {x} {op} {y} = {result}")

    print(f"\n缓存统计: {complex_calculation.cache_info()}")


def demo_cache_size_effects():
    """缓存大小效果演示"""
    print("\n\n=== 5. 缓存大小效果演示 ===")

    @lru_cache(maxsize=5)  # 小缓存
    def small_cache_func(n: int) -> int:
        """小缓存函数"""
        time.sleep(0.01)
        return n * 2

    @lru_cache(maxsize=50)  # 大缓存
    def large_cache_func(n: int) -> int:
        """大缓存函数"""
        time.sleep(0.01)
        return n * 2

    # 测试数据：10个不同值的重复访问
    test_values = [i % 10 for i in range(100)]

    # 小缓存测试
    start = time.time()
    for val in test_values:
        small_cache_func(val)
    small_cache_time = time.time() - start
    small_cache_info = small_cache_func.cache_info()

    # 大缓存测试
    start = time.time()
    for val in test_values:
        large_cache_func(val)
    large_cache_time = time.time() - start
    large_cache_info = large_cache_func.cache_info()

    print("缓存大小对比:")
    print(
        f"  小缓存(5): 耗时{small_cache_time:.2f}s, 命中率{small_cache_info.hits / (small_cache_info.hits + small_cache_info.misses) * 100:.1f}%"
    )
    print(
        f"  大缓存(50): 耗时{large_cache_time:.2f}s, 命中率{large_cache_info.hits / (large_cache_info.hits + large_cache_info.misses) * 100:.1f}%"
    )


def main():
    """运行所有演示"""
    print("🗄️ LRU缓存 (@lru_cache) 教程")
    print("=" * 50)

    demo_basic_usage()
    demo_cache_management()
    demo_database_query()
    demo_complex_parameters()
    demo_cache_size_effects()

    print("\n" + "=" * 50)
    print("📝 关键要点:")
    print("1. 适用于有重复调用的函数")
    print("2. 参数必须是可哈希的")
    print("3. maxsize 控制缓存大小")
    print("4. cache_info() 查看统计信息")
    print("5. cache_clear() 清理缓存")
    print("6. LRU算法自动管理内存")


if __name__ == "__main__":
    main()
