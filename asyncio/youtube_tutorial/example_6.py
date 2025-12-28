import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def fetch_data(param):
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"


async def main():
    # Run in Threads
    # 多线程立刻开始工作, 不用等 main() await 放弃控制权
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))
    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")

    # Run in Process Pool (两种方式效果一致)
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        # 多进程立刻开始工作, 不用等 main() await 放弃控制权
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        # 这里 await 的作用仅仅是控制输出顺序,实际上 Event Loop 中没有其他任务供它调度了
        # Event Loop 对子线程中的任务调度完全没有权限
        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]


if __name__ == "__main__":
    t1 = time.perf_counter()

    results = asyncio.run(main())
    print(results)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1:.2f} seconds")
