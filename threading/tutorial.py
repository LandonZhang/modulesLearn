from threading import Thread
import time

DONE = False
counter = 0


# def work():
#     global counter, DONE
#     while not DONE:
#         counter += 1
#         time.sleep(1)
#         print(counter)


# 不启用多线程，无法达到退出的效果
# work()

# 启动一个单独的线程
# Thread(target=work).start()


# def work(arg: str):
#     global counter, DONE
#     while not DONE:
#         counter += 1
#         time.sleep(1)
#         print(f"{arg} : {counter}")


# 使用 args 进行传参
# Thread(target=work, args=("ABC",)).start()
# Thread(target=work, args=("XYZ",)).start()


# 使用 daemon 创建守护进程 (当重要进程停止时，守护进程自动关闭)
# def work(arg: str):
#     global counter
#     while True:
#         counter += 1
#         time.sleep(1)
#         print(f"{arg} : {counter}")


# Thread(target=work, daemon=True, args=("ABC",)).start()


def work(arg: str):
    global counter, DONE
    while not DONE:
        counter += 1
        time.sleep(1)
        print(f"{arg} : {counter}")


# 使用 join 函数来控制当线程完成时才进行到下一部
t1 = Thread(target=work, args=("ABC",))
t2 = Thread(target=work, args=("XYZ",))

t1.start()
t2.start()

t1.join()
t2.join()

input("Please enter something to quit")
DONE = True
