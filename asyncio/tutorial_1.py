import asyncio
import time


async def wait(sleep_time: int, id: int):
    print(f"id:{id} is start.")
    await asyncio.sleep(sleep_time)
    print(f"id:{id} is wake up.")
    return {"id": id, "time": sleep_time}


async def main():
    print("Coroutine is started.")

    # 没有使用 task, 导致就算交出了控制权. Eventloop 也不会执行其他的动作
    # 而是等待任务1完成，导致 async 操作失效
    await wait(1, 1)
    await wait(2, 2)
    await wait(3, 3)

    print("Coroutine is ended")


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    time_cost = end_time - start_time
    print(f"The time cost is {time_cost: .2f} s")  # 6 seconds
