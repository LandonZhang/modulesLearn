import asyncio
import time


async def wait(sleep_time: int, id: int):
    print(f"id:{id} is start.")
    await asyncio.sleep(sleep_time)
    print(f"id:{id} is wake up.")
    return {"id": id, "time": sleep_time}


async def main():
    print("Coroutine is started.")

    # create_task 会创建 task 并启动一个 coroutine (但如果不 await 的话就没人在意这个任务是否完成了)
    # task1 = asyncio.create_task(wait(2, 1))
    # task2 = asyncio.create_task(wait(3, 2))
    # task3 = asyncio.create_task(wait(1, 3))

    # await 等待结果
    # await task1
    # await task2
    # await task3

    # gather 只是并发创建并启动了多个任务，需要 await 来等待这些任务返回结果
    results = await asyncio.gather(wait(2, 1), wait(3, 2), wait(1, 3))

    print(results)
    # for result in results:
    #     print(result)

    print("Coroutine is ended")


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    time_cost = end_time - start_time
    print(f"The time cost is {time_cost: .2f} s")  # 3 seconds
