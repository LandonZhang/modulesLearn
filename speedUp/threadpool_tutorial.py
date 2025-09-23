# -*- coding: utf-8 -*-
"""
线程池 (ThreadPoolExecutor) 教程
==============================

学习如何使用线程池来提升程序性能
"""

import time
import threading
import concurrent.futures
import random


def demo_basic_usage():
    """基础使用演示"""
    print("=== 1. 基础使用演示 ===")

    def slow_task(task_id: int) -> str:
        """模拟耗时任务"""
        print(f"  任务 {task_id} 开始执行")
        time.sleep(1)  # 模拟1秒工作
        print(f"  任务 {task_id} 完成")
        return f"任务{task_id}的结果"

    # 串行执行
    print("\n串行执行:")
    start = time.time()
    results = [slow_task(i) for i in range(1, 4)]
    serial_time = time.time() - start
    print(f"串行耗时: {serial_time:.2f}秒")

    # 并行执行
    print("\n并行执行:")
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # submit 之后任务立刻在空闲线程开始执行
        futures = [executor.submit(slow_task, i) for i in range(4, 7)]
        # .result() 获得结果的方式会按 future 顺序返回结果 (即使后面的任务已经完成也得等前面的任务完成再输出)
        results = [future.result() for future in futures]
    parallel_time = time.time() - start
    print(f"并行耗时: {parallel_time:.2f}秒")
    print(f"性能提升: {serial_time / parallel_time:.1f}倍")


def demo_as_completed():
    """as_completed 使用演示"""
    print("\n\n=== 2. as_completed 使用演示 ===")

    def random_task(task_id: int) -> str:
        """随机耗时任务"""
        duration = random.uniform(0.5, 2.0)
        time.sleep(duration)
        return f"任务{task_id} (耗时{duration:.1f}s)"

    print("按完成顺序收集结果:")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 任务映射字典
        future_to_id = {executor.submit(random_task, i): i for i in range(1, 6)}

        # .as_completed() 按完成顺序返回结果 (完成一个就返回一个)
        for future in concurrent.futures.as_completed(future_to_id):
            task_id = future_to_id[future]
            result = future.result()
            print(f"  收到: {result}")


def demo_error_handling():
    """错误处理演示"""
    print("\n\n=== 3. 错误处理演示 ===")

    def unreliable_task(task_id: int) -> str:
        """不可靠的任务"""
        if random.random() < 0.3:  # 30%失败率
            raise Exception(f"任务{task_id}失败")
        return f"任务{task_id}成功"

    successful = []
    failed = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_id = {executor.submit(unreliable_task, i): i for i in range(1, 8)}

        for future in concurrent.futures.as_completed(future_to_id):
            task_id = future_to_id[future]
            try:
                result = future.result()
                successful.append(result)
                print(f"  ✅ {result}")
            except Exception as e:
                failed.append((task_id, str(e)))
                print(f"  ❌ 任务{task_id}: {e}")

    print(f"\n结果: 成功{len(successful)}个, 失败{len(failed)}个")


# 提供了 map 函数供我们 submit 和 .result() 一起做 (按顺序返回结果)
def slow_task(x):
    time.sleep(3 - x)  # 模拟不同耗时
    return x


def map_demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        # 将 1, 2, 3 分别传入 slow_task 中并执行 (按顺序返回结果, 就算 3 先完成也得等 1)
        for result in ex.map(slow_task, [1, 2, 3]):
            print("结果:", result)


def as_completed_demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        # 创建三个 future 并执行
        futures = [ex.submit(slow_task, x) for x in [1, 2, 3]]
        # 谁先完成谁先返回
        for result in concurrent.futures.as_completed(futures):
            print("结果:", result.result())


def main():
    """运行所有演示"""
    print("🧵 线程池 (ThreadPoolExecutor) 教程")
    print("=" * 50)

    # demo_basic_usage()
    # demo_as_completed()
    # demo_error_handling()
    # demo_practical_example()
    print("=== map 演示 ===")
    map_demo()
    print("=== as_completed 演示 ===")
    as_completed_demo()

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
