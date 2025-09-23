import logging

# 配置根日志记录器 (默认创建的 root logger，为 stream handler)
# name 将会为子 logger 向上传播时的 name，即: myapp.moduleA
logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

# 创建一个子日志记录器
logger_a = logging.getLogger("myapp.moduleA")
logger_a.propagate = False  # 关闭向上传播，到 logger_a 停止
# 创建一个文件处理器
file_handler = logging.FileHandler("moduleA.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
# 将文件处理器添加到子日志记录器
logger_a.addHandler(file_handler)

# 通过向上传递，同时被 looger_a 和 root 处理
# 设置了 propagate 之后不再在控制台输出
logger_a.info("The last of US is a fucking good game.")
