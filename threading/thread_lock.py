import threading
import time


class TestClass:
    # 类属性
    _shared_object = None
    _lock = threading.Lock()

    @classmethod
    def get_shared_object(cls):
        if cls._shared_object is None:
            # 加锁，在多线程中，保证只有一个线程能够创建对象
            with cls._lock:
                if cls._shared_object is None:
                    print(f"线程 {threading.current_thread().name} 正在创建对象")
                    time.sleep(0.1)  # 模拟创建耗时
                    cls._shared_object = "共享对象"
                    print(f"线程 {threading.current_thread().name} 创建完成")
                else:
                    print(f"线程 {threading.current_thread().name} 发现对象已存在")
        return cls._shared_object


# 创建多个线程测试
threads = []
for i in range(5):
    t = threading.Thread(target=TestClass.get_shared_object, name=f"Thread-{i}")
    threads.append(t)

# 同时启动所有线程
for t in threads:
    t.start()

# 等待线程完成
for t in threads:
    t.join()
