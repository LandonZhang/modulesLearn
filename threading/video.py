from threading import Thread
import time

DONE = False
counter = 0


# 使用 daemon 创建守护进程 (当重要进程停止时，守护进程自动关闭)
def work(arg: str):
    global counter
    while True:
        counter += 1
        time.sleep(1)
        print(f"{arg} : {counter}")


Thread(target=work, daemon=True, args=("ABC",)).start()
input("Please enter something to quit")
DONE = True
