### cProfile 使用

```bash
python -m cProfile -o profile_output.prof real_world_example_async_v1.py
```

生成的 `.prof` 文件可以通过 `snakeviz`来可视化查看（不带 -o 则是直接输出到控制台中）

```bash
snakeviz profile_output.prof
```

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
