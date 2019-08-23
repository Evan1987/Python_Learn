"""
Process之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。
Python的 multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据。
我们以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据：
"""

import os, time, random
from multiprocessing import Process, Queue


def write(q: Queue):
    print(f"Process to write: {os.getpid()}")
    for value in ["A", "B", "C"]:
        print(f"Put {value} to queue...")
        q.put(value)
        time.sleep(random.random())


def read(q: Queue):
    print(f"Process to read: {os.getpid()}")
    while True:  # 死循环
        value = q.get(True)
        print(f"Get {value} from queue.")


if __name__ == "__main__":
    q = Queue()
    pw = Process(target=write, args=(q, ))
    pr = Process(target=read, args=(q, ))

    pw.start()
    pr.start()
    pw.join()

    pr.terminate()  # 强行终止
