from threading import Thread
import time

DONE = False
counter = 0


def work(arg: str):
    global counter, DONE
    while not DONE:
        counter += 1
        time.sleep(1)
        print(f"{arg} : {counter}")


# 使用 join 函数来控制当线程完成时才进行到下一步
t1 = Thread(target=work, args=("ABC",), name="thread-1")
t2 = Thread(target=work, args=("XYZ",), name="thread-2")

t1.start()
t1.join()  # 由于 t1 永远不会停止，故到不了 input 那一步
print(f"thread-1 is done")

t2.start()
t2.join()
print(f"thread-2 is done")


input("Please enter something to quit")
DONE = True
