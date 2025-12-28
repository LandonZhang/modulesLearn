# Python 性能优化教程：线程池 & LRU缓存

## 📚 教程概述

本教程分别演示如何使用 `concurrent.futures.ThreadPoolExecutor` 和 `functools.lru_cache` 来提升 Python 程序性能。

## 🎯 学习目标

- 掌握线程池的基本使用方法
- 理解LRU缓存的工作原理
- 学会将两者结合应用到实际项目

## 📖 教程文件

### 1. `threadpool_tutorial.py` - 线程池教程

- 基础使用演示（串行 vs 并行）
- `as_completed()` 按完成顺序处理
- 错误处理和异常管理
- 实际应用示例（批量数据处理）

### 2. `lru_cache_tutorial.py` - LRU缓存教程

- 基础使用演示（有缓存 vs 无缓存）
- 缓存管理（统计信息、清理缓存）
- 数据库查询缓存示例
- 复杂参数缓存演示
- 缓存大小效果对比

### 3. `combined_example.py` - 综合应用示例

- 线程池 + LRU缓存结合使用
- 模拟真实业务场景（订单处理系统）
- 串行 vs 并行处理对比
- 缓存效果验证

## 🚀 快速开始

```bash
# 运行线程池教程
python threadpool_tutorial.py

# 运行LRU缓存教程  
python lru_cache_tutorial.py

# 运行综合应用示例
python combined_example.py
```

**环境要求**：Python 3.6+（无需额外依赖）

## 💡 核心概念

### 线程池 (ThreadPoolExecutor)

- **适用场景**：I/O密集型任务（网络请求、数据库查询）
- **核心优势**：并发执行、自动线程管理、内置错误处理
- **基本用法**：

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, data) for data in data_list]
    for future in as_completed(futures):
        result = future.result()
```

### LRU缓存 (lru_cache)

- **适用场景**：重复计算或查询的函数
- **核心优势**：自动缓存、LRU算法、透明优化
- **基本用法**：

```python
@lru_cache(maxsize=128)
def expensive_function(param):
    # 耗时操作
    return result
```

## 📊 性能提升效果

| 场景           | 优化前 | 优化后 | 提升倍数 |
| -------------- | ------ | ------ | -------- |
| 4个并发任务    | 8秒    | 2秒    | 4倍      |
| 重复数据库查询 | 1000ms | 50ms   | 20倍     |

## ⚠️ 注意事项

**线程池**：

- 适用于I/O密集型任务
- 合理设置线程数（CPU核心数的2-4倍）
- 注意错误处理

**LRU缓存**：

- 函数参数必须可哈希
- 设置合适的maxsize
- 考虑缓存失效策略

## 🚀 `future` 对象

Future 还有几个会用到的功能：

1. `cancel():`

* 作用：尝试取消任务。
* 限制：只有任务还在排队（还没被子进程领走）时才能取消。一旦开始运行就停不下来了（Python 无法强制杀死运行中的线程/进程）。

2. `running() / done():`

* 作用：非阻塞地查询状态。“你做完了吗？”“还在跑吗？”
* 场景：写即时进度条或者监控面板时有用。

3. `result(timeout=5):`

* 作用：设置超时时间。
* 场景：如果某个任务卡死（死循环），你不希望主进程一直等下去，可以设置超时，超时后会抛出 TimeoutError。
