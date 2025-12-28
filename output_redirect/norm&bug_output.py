print("This is a norm sentence")

print("There is something about to happen")

print(1 / 0)

# 执行命令：python '.\norm&bug_output.py' >> debug.log
# 将输出定向到 log 文件，但是报错没有

# 执行命令：python '.\norm&bug_output.py' >> debug1.log 2>&1
# 将报错也重定向

# 执行命令：python '.\norm&bug_output.py'  2>&1 | tee debug2.log
# 即重定向又显示在终端
