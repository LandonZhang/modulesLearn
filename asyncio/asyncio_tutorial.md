# Python asyncio 异步编程教程

本教程基于 [YouTube 视频](https://www.youtube.com/watch?v=oAkLSJNr5zY) 学习内容，通过实际代码示例逐步掌握 Python asyncio 异步编程。例子配有十分好理解的 [动画演示](https://coreyms.com/asyncio/)

## 目录

1. [基础概念](#基础概念)
2. [协程函数与协程对象](#协程函数与协程对象)
3. [同步 vs 立即 await](#同步-vs-立即-await)
4. [任务创建与调度](#任务创建与调度)
5. [任务执行顺序](#任务执行顺序)
6. [常见陷阱：阻塞操作](#常见陷阱阻塞操作)
7. [线程和进程池](#线程和进程池)
8. [高级并发控制](#高级并发控制)
9. [实际应用案例](#实际应用案例)

## 基础概念

### 核心术语理解

在开始学习 asyncio 之前，需要理解几个关键概念：

**协程函数 (Coroutine Function)**

- 使用 `async def` 定义的函数
- 调用协程函数不会立即执行，而是返回一个协程对象

**协程对象 (Coroutine Object)**

- 协程函数被调用时返回的对象
- 是可等待对象 (awaitable)，需要通过 `await` 或事件循环来执行

**任务 (Task)**

- 协程对象的包装器，用于在事件循环中调度执行
- 底层基于 Future 对象
- 也是可等待对象 (awaitable)

**Future**

- 表示异步操作最终结果的对象
- 具有几个重要状态：
  - `pending`: 尚未执行
  - `exception`: 发生异常
  - `result`: 得到结果
  - `stop`: 暂停

**Event Loop** 什么时候才能调度一个 Coroutine Object?

1. 主动调用 `asyncio.run()`
2. 主动等待 `await`
3. 将 Corountine Object 加入任务队列 `create_task()`，Event Loop 在其他任务因为 IO 任务暂停时不会**闲着**，而是看还有没有任务可以进行执行（此为并行调度的关键！）
4. 使用 `asyncio.gather` 或者 `asyncio.TaskGroup` 集中创建 tasks

## 协程函数与协程对象

让我们从最基本的例子开始理解协程：

```python
import asyncio
import time

def sync_function(test_param: str) -> str:
    print("This is a synchronous function.")
    time.sleep(0.1)  # 阻塞操作
    return f"Sync Result: {test_param}"

# 这是一个协程函数
async def async_function(test_param: str) -> str:
    print("This is an asynchronous coroutine function.")
    await asyncio.sleep(0.1)  # 非阻塞操作
    return f"Async Result: {test_param}"

async def main():
    # 同步函数调用
    sync_result = sync_function("Test")
    print(sync_result)

    # 协程对象创建
    coroutine_obj = async_function("Test")
    print(coroutine_obj)  # 输出: <coroutine object async_function at 0x...>

    # 等待协程执行
    coroutine_result = await coroutine_obj
    print(coroutine_result)

if __name__ == "__main__":
    asyncio.run(main())
```

**关键理解点：**

- `async def` 定义的是协程函数，调用它返回的是协程对象（coroutine awaitable）
- 协程对象本身不会执行，需要通过 `await` 或事件循环来驱动执行

## 同步 vs 立即 await

### 同步版本 (Example 1)

```python
import time

def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)  # 阻塞等待
    print(f"Done with {param}")
    return f"Result of {param}"

def main():
    result1 = fetch_data(1)    # 必须等待1秒
    print("Fetch 1 fully completed")
    result2 = fetch_data(2)    # 必须等待2秒
    print("Fetch 2 fully completed")
    return [result1, result2]

# 总执行时间：3秒（1+2）
```

### 异步版本但立即 await (Example 2)

```python
import asyncio
import time

async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)  # 非阻塞等待
    print(f"Done with {param}")
    return f"Result of {param}"

async def main():
    task1 = fetch_data(1)      # 创建协程对象
    task2 = fetch_data(2)      # 创建协程对象

    result1 = await task1      # 立即等待，没有并发
    print("Task 1 fully completed")
    result2 = await task2      # 立即等待，没有并发
    print("Task 2 fully completed")
    return [result1, result2]

# 总执行时间：仍然是3秒
```

**关键理解点：**

- 创建协程对象后立刻 `await`，由于没有将任务放入 event loop 调度，导致和同步调用没有差异
- 虽然使用了异步语法，但实际执行仍然是顺序的

## 任务创建与调度

### 正确的异步方式 (Example 3)

```python
import asyncio
import time

async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"

async def main():
    # 使用 create_task 将协程调度到事件循环
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # 等待任务完成
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]

# 总执行时间：2秒（并发执行）
```

**关键理解点：**

- `asyncio.create_task()` 将协程调度提前加入 event loop 进行调度，但不会立即启动执行
- 任务在事件循环中并发执行，可以实现真正的异步
- 总耗时2s，结合动画理解即可

## 任务执行顺序

### 改变等待顺序 (Example 4)

```python
async def main():
    task1 = asyncio.create_task(fetch_data(1))  # 1秒任务
    task2 = asyncio.create_task(fetch_data(2))  # 2秒任务

    # 先等待较长的任务
    result2 = await task2  # 等待2秒任务完成
    print("Task 2 fully completed")
    result1 = await task1  # task1 已经完成了
    print("Task 1 fully completed")
    return [result1, result2]
```

**关键理解点：**

- `await` 交出控制权之后不一定就会立刻执行你写在后面的函数（按照 coroutine ready 的顺序执行）
- 但一定会保证等到你指定的函数执行完再向下走

## 常见陷阱：阻塞操作

### 错误示例 (Example 5)

```python
import asyncio
import time

async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)  # ❌ 错误：在异步函数中使用阻塞操作
    print(f"Done with {param}")
    return f"Result of {param}"

# 即使使用了 create_task，仍然会阻塞
```

**关键点：**

- 在异步函数中使用 `time.sleep()` 会阻塞整个事件循环
- 必须使用 `await asyncio.sleep()` 来实现非阻塞等待

## 线程和进程池

### 何时使用多线程处理 I/O 任务

使用多线程处理 I/O 任务通常有两个主要原因：

1. **现有代码结构复杂**：使用 `async/await` 重构开销过大，希望快速通过并发执行来提升性能98
2. **库不支持异步**：当前使用的第三方库没有异步版本支持，不得不借助多线程实现并发操作

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

def fetch_data(param):  # 普通的阻塞函数（比如使用 requests 库）
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)  # 模拟 I/O 等待
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"

async def main():
    # 在线程中运行阻塞的 I/O 函数
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))

    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")
```

### 何时使用多进程

使用多进程的场景相对简单明确：

**CPU 密集型任务**：任务需要大量的运算处理，多线程由于 GIL（全局解释器锁）的存在，无法真正实现并发操作。因为一个线程占用 GIL 的时间很长，其他线程只能等待。

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_intensive_task(n):
    """CPU 密集型任务示例：计算素数"""
    count = 0
    for i in range(2, n):
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                break
        else:
            count += 1
    return count

async def main():
    # CPU 密集型任务必须使用进程池
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, cpu_intensive_task, 10000)
        task2 = loop.run_in_executor(executor, cpu_intensive_task, 15000)

        result1 = await task1
        print(f"Process 1 completed: {result1} primes")
        result2 = await task2
        print(f"Process 2 completed: {result2} primes")
```

### 性能分析工具：scalene

对于不清楚代码瓶颈在哪里的情况，可以使用 **scalene** 工具来分析性能：

```bash
# 安装 scalene
pip install scalene

# 运行性能分析
scalene script.py --outfile result.scl
scalene --viewer result.scl
```

**scalene 的关键指标：**

- **系统时间**：等待 I/O 服务的时间（文件读写、网络请求等）
- **Python 时间**：Python 代码实际执行时间

**scalene 中定义的三类时间：**

* **Python** ：纯 Python 解释器干活的时间（纯 Python for 循环、列表推导、自己写的逻辑） → 想 CPU 并行就考虑 **多进程 / 改算法 / 调库**
* **native** ：C/C++ 扩展干活的时间（`numpy` 运算） → 多线程可能收益很大
* **system** ：在系统里睡觉/等 I/O 的时间（文件读写、数据库访问、`request`） → 典型  **I/O 绑定** ，适合多线程 / 异步

**基于分析结果选择优化策略：**

```python
# 伪代码示例
if 系统时间占比高:
    # I/O 密集型任务
    if 现有库支持异步:
        使用_async_await()
    else:
        使用_多线程(asyncio.to_thread)
elif Python时间占比高:
    # CPU 密集型任务
    使用_多进程(ProcessPoolExecutor)
else:
    # 混合型任务
    根据具体情况选择合适的策略()
```

**实际示例：分析和优化决策**

```python
# 原始同步代码
import requests
import time

def download_and_process():
    # I/O 操作：网络请求
    response = requests.get("https://api.example.com/data")
    data = response.json()

    # CPU 操作：数据处理
    processed = complex_calculation(data)
    return processed

# 根据 scalene 分析结果优化：
# 如果网络请求占用大部分时间 -> 使用多线程或异步
# 如果数据处理占用大部分时间 -> 使用多进程
```

## 高级并发控制

### asyncio.gather()

```python
async def main():
    # 创建多个协程
    coroutines = [fetch_data(i) for i in range(1, 3)]

    # gather 可以自动将协程对象转换为任务对象
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(f"Coroutine Results: {results}")

    # 也可以用于任务
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Task Results: {results}")
```

**使用场景：** 当希望一个任务错误不会影响其他任务执行时使用 `gather`

### asyncio.TaskGroup()

```python
async def main():
    # TaskGroup 确保所有任务必须成功
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
        # 所有任务在上下文管理器退出时自动等待

    print(f"Task Group Results: {[result.result() for result in results]}")
```

**使用场景：** 当希望全部任务必须成功，只要有一个错误就停止所有任务时，使用 TaskGroup

**注意：** TaskGroup 创建的任务不需要手动 `await`，在创建之后就会自动 `await`

## 实际应用案例

让我们通过一个图片下载和处理的例子来看 asyncio 的实际应用：

### 同步版本的问题

```python
def download_images(urls):
    with requests.Session() as session:
        img_paths = [
            download_single_image(session, url, img_num)
            for img_num, url in enumerate(urls, start=1)
        ]
    return img_paths

def process_images(orig_paths):
    img_paths = [process_single_image(orig_path) for orig_path in orig_paths]
    return img_paths

# 所有操作都是串行的，效率低下
```

### 异步优化版本 1：基础异步

```python
async def download_images(urls):
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(asyncio.to_thread(download_single_image, url, img_num))
            for img_num, url in enumerate(urls, start=1)
        ]
    img_paths = [task.result() for task in tasks]
    return img_paths

async def process_images(orig_paths):
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(asyncio.to_thread(process_single_image, orig_path))
            for orig_path in orig_paths
        ]
    img_paths = [task.result() for task in tasks]
    return img_paths
```

### 异步优化版本 2：真正的异步 I/O

```python
import aiofiles
import httpx

async def download_single_image(client: httpx.AsyncClient, url: str, img_num: int):
    print(f"Downloading {url}...")
    response = await client.get(url, timeout=10, follow_redirects=True)
    response.raise_for_status()

    filename = f"image_{img_num}.jpg"
    download_path = ORIGINAL_DIR / filename

    # 异步文件操作
    async with aiofiles.open(download_path, "wb") as f:
        # async for: 异步迭代器，每次迭代会 await 数据准备
        async for chunk in response.aiter_bytes(chunk_size=8192):
            await f.write(chunk)

    print(f"Downloaded and saved to: {download_path}")
    return download_path

async def download_images(urls):
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(download_single_image(client, url, img_num))
                for img_num, url in enumerate(urls, start=1)
            ]
        img_paths = [task.result() for task in tasks]
    return img_paths
```

**异步 I/O 的关键点：**

- `async for` 的核心区别：它会自动等待一个 awaitable 的结果，适合处理流式、逐步产生结果的场景
- 使用 `httpx` 代替 `requests` 进行异步 HTTP 请求
- 使用 `aiofiles` 进行异步文件操作

### 异步优化版本 3：并发控制

```python
async def download_single_image(
    client: httpx.AsyncClient,
    url: str,
    img_num: int,
    semaphore: asyncio.Semaphore  # 信号量控制并发数
):
    async with semaphore:  # 限制同时下载的数量
        # ... 下载逻辑
        pass

async def download_images(urls):
    DOWNLOAD_LIMIT = 4  # 最多同时下载4个文件
    dl_semaphore = asyncio.Semaphore(DOWNLOAD_LIMIT)

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    download_single_image(client, url, img_num, dl_semaphore)
                )
                for img_num, url in enumerate(urls, start=1)
            ]
        img_paths = [task.result() for task in tasks]
    return img_paths
```

**并发控制的重要性：**

- 使用 `asyncio.Semaphore` 限制同时执行的任务数量
- 避免过多并发请求导致服务器拒绝服务或系统资源耗尽

## 最佳实践总结

1. **正确使用协程和任务**

   - 使用 `asyncio.create_task()` 来调度协程到事件循环
   - 避免立即 `await` 协程对象
2. **避免阻塞操作**

   - 在异步函数中使用 `await asyncio.sleep()` 而不是 `time.sleep()`
   - 使用异步库（如 `httpx`, `aiofiles`）进行 I/O 操作
3. **合理的并发控制**

   - 使用 `asyncio.Semaphore` 控制并发数量
   - 根据任务性质选择 `gather` 或 `TaskGroup`
4. **CPU 密集型任务处理**

   - 使用  `loop.run_in_executor()`
   - 将 CPU 密集型任务交给进程池
5. **错误处理**

   - 使用 `return_exceptions=True` 在 `gather` 中处理异常
   - 使用 `TaskGroup` 确保任务组的原子性
6. **性能分析与优化决策**

   - 使用 `scalene` 工具分析系统时间和 Python 时间
   - 根据分析结果选择合适的并发策略

通过理解这些核心概念和最佳实践，你就能够有效地使用 asyncio 来编写高性能的异步 Python 程序！ 🚀
