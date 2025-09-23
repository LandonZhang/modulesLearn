import asyncio
import time


async def fetch_data(param):
    await asyncio.sleep(param)
    return f"Result of {param}"


async def main():
    # Create Tasks Manually
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    result2 = await task2
    print(f"Task 1 and 2 awaited results: {[result1, result2]}")

    # Gather Coroutines
    coroutines = [fetch_data(i) for i in range(1, 3)]
    # 默认不返回异常
    # gather 可以自动将 co-routine object 转换为 task object
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(f"Coroutine Results: {results}")

    # Gather Tasks
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]
    # 在希望一个任务错误不会影响其他任务执行时使用 gather
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Task Results: {results}")

    # Task Group
    # 在希望全部任务必须成功，只要有一个错误就停止所有任务时，使用 task group
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
        # All tasks are awaited when the context manager exits.
    print(f"Task Group Results: {[result.result() for result in results]}")

    return "Main Coroutine Done"


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")
