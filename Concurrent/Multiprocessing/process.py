import os
from multiprocessing import Process


def run_proc(name: str):
    print(f"Run child process {name} ({os.getpid()})")


if __name__ == "__main__":
    print(f"Parent process {os.getpid()}")
    p = Process(target=run_proc, args=("test", ))
    print("Child process will start")
    p.start()
    p.join()
    print("Child process end.")
