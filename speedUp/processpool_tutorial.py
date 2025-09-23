from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import time


def cpu_heavy(n: int) -> tuple[int, float, int]:
    s = sum(i * i for i in range(n))
    # getpid() 获得当前进程的 id
    return n, s**0.5, os.getpid()


if __name__ == "__main__":
    print("多线程版本运行")
    start_time = time.perf_counter()
    nums = [10_000_000, 12_000_000, 9_000_000, 15_000_000]

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        # 提交任务并启动多线程执行
        futures = [ex.submit(cpu_heavy, n) for n in nums]

        # 按照完成顺序收集结果
        for fut in as_completed(futures):
            n, ans, pid = fut.result()
            print(f"n={n}  ans≈{ans:.1f}  by PID={pid}")

    end_time = time.perf_counter()
    time_cost = end_time - start_time
    print(f"The time cost is {time_cost: .2f} s")
    print("多线程版本结束")

    print("单线程版本运行")
    start_time = time.perf_counter()
    for n in nums:
        n, ans, pid = cpu_heavy(n)
        print(f"n={n}  ans≈{ans:.1f}  by PID={pid}")
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    print(f"The time cost is {time_cost: .2f} s")
    print("单线程版本结束")
