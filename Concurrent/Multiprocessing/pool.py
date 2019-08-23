import os, time, random
from multiprocessing import Pool


def long_time_task(name: str):
    print(f"Run task {name} ({os.getpid()})")
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f"Task {name} runs {(end - start):.2f} seconds.")


if __name__ == "__main__":
    print(f"Parent process {os.getpid()}.")
    p = Pool(4)
    for i in range(5):
        p.apply_async(func=long_time_task, args=(i, ))
    print("Waiting for all subprocess done.")
    p.close()  # 调用close()之后就不能继续添加新的Process了。
    p.join()  # 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()
    print("All subprocess done.")
