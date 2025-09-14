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
        futures = [executor.submit(slow_task, i) for i in range(4, 7)]
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

        # 按完成顺序处理结果
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


def demo_practical_example():
    """实际应用示例"""
    print("\n\n=== 4. 实际应用示例：批量数据处理 ===")

    def process_data(data_id: int) -> dict:
        """模拟数据处理"""
        # 模拟API调用或数据库查询
        time.sleep(random.uniform(0.1, 0.3))

        return {
            "id": data_id,
            "result": f"处理结果_{data_id}",
            "status": "完成",
            "thread": threading.current_thread().name,
        }

    # 要处理的数据
    data_ids = list(range(1, 11))  # 10个数据项

    print(f"处理 {len(data_ids)} 个数据项...")
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务
        future_to_id = {
            executor.submit(process_data, data_id): data_id for data_id in data_ids
        }

        # 收集结果
        results = []
        for future in concurrent.futures.as_completed(future_to_id):
            data_id = future_to_id[future]
            try:
                result = future.result()
                results.append(result)
                print(f"  数据{data_id} 完成 - 线程: {result['thread']}")
            except Exception as e:
                print(f"  数据{data_id} 失败: {e}")

    process_time = time.time() - start
    print(f"\n处理完成: {len(results)}个成功, 总耗时{process_time:.2f}秒")


def main():
    """运行所有演示"""
    print("🧵 线程池 (ThreadPoolExecutor) 教程")
    print("=" * 50)

    demo_basic_usage()
    # demo_as_completed()
    # demo_error_handling()
    # demo_practical_example()

    print("\n" + "=" * 50)
    print("📝 关键要点:")
    print("1. 适用于 I/O 密集型任务")
    print("2. max_workers 控制并发数量")
    print("3. as_completed() 按完成顺序处理")
    print("4. 使用字典映射追踪任务")
    print("5. 注意错误处理和异常管理")


if __name__ == "__main__":
    main()
