### cProfile 使用

```bash
python -m cProfile -o profile_output.prof real_world_example_async_v1.py
```

生成的 `.prof` 文件可以通过 `snakeviz`来可视化查看（不带 -o 则是直接输出到控制台中）

```bash
snakeviz profile_output.prof
```

文件字段解析

| 列名                      | 含义                         |
| ------------------------- | ---------------------------- |
| ncalls                    | 调用次数                     |
| tottime                   | 函数自身耗时，不含子函数调用 |
| percall(1)                | tottime / ncalls             |
| cumtime                   | 函数总耗时，含子调用         |
| percall(2)                | cumtime / ncalls             |
| filename:lineno(function) | 位置与函数名                 |

典型分析：

- 如果一个函数的 tottime 高 → 它自己内部计算慢。
- 如果 tottime 低但 cumtime 高 → 它花时间花在它调用的其他函数身上。

在 python 代码中内嵌使用

```python
if __name__ == "__main__":
	profile = cProfile.Profile()
     	profile.enable()  # 开始分析
	main()
	profile.disable()  # 结束分析
	# 保存结果
	profile.dump_stats(result.prof)  # 保存结果
```
