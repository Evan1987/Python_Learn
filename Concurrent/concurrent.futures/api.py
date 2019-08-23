
"""
concurrent.futures 源码解析
source: https://www.cnblogs.com/kangoroo/p/7628092.html
"""

import _utils.context as _context
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor,\
    as_completed, wait, FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED


def gcd(pair):
    a, b = pair
    low = min(a, b)
    if a % low == 0 and b % low == 0:
        return low
    start = low // 2
    for i in range(start, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


numbers = [(1963309, 2265973), (1879675, 2493670), (2030677, 3814172),
           (1551645, 2229620), (1988912, 4736670), (2198964, 7876293)]


if __name__ == "__main__":

    """1. map(self, fn, *iterables, **kwargs)"""
    """返回的results列表是有序的，顺序和 `*iterables` 迭代器的顺序一致。"""
    with _context.timer("Map test"):
        with ProcessPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(gcd, numbers))
        print(results)

    """2. submit(self, fn, *args, **kwargs)"""
    """用于提交一个可并行的方法，submit方法同时返回一个future实例。"""
    """future对象标识这个线程/进程异步进行，并在未来的某个时间执行完成。future实例表示线程/进程状态的回调。"""
    with _context.timer("Submit test"):
        futures = []
        with ProcessPoolExecutor(max_workers=2) as pool:
            for pair in numbers:
                future = pool.submit(gcd, pair)
                futures.append(future)
        results = [future.result() for future in futures]
        print(results)

    """3. future"""
    """future提供了跟踪任务执行状态的方法。如判断任务是否执行中future.running()，判断任务是否执行完成future.done()等等。
        as_completed方法传入futures迭代器和timeout两个参数,默认timeout=None，阻塞等待任务执行完成，并返回执行完成的future对象迭代器.
        迭代器是通过yield实现的。timeout>0，等待timeout时间，如果timeout时间到仍有任务未能完成，不再执行并抛出异常TimeoutError"""
    with _context.timer("future api test"):
        with ProcessPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(gcd, pair) for pair in numbers]
            for future in futures:
                print(f"Running: {future.running()}, Done: {future.done()}")
            print("*" * 10)
            for future in as_completed(futures, timeout=2):
                print(f"Running: {future.running()}, Done: {future.done()}")

    """4. wait"""
    """wait方法接会返回一个tuple，tuple中包含两个set，一个是completed(已完成的)另外一个是uncompleted(未完成的)。
        使用wait方法的一个优势就是获得更大的自由度，它接收三个参数FIRST_COMPLETED, FIRST_EXCEPTION和ALL_COMPLETE，默认为ALL_COMPLETED。"""
    with _context.timer("wait api test"):
        with ProcessPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(gcd, pair) for pair in numbers]
            for future in futures:
                print(f"Running: {future.running()}, Done: {future.done()}")
            print("*" * 10)
            # 由于设置了ALL_COMPLETED，所以wait等待所有的task执行完成，可以看到6个任务都执行完成了。
            # 如果我们将配置改为FIRST_COMPLETED，wait会等待直到第一个任务执行完成，返回当时所有执行成功的任务。
            done, unfinished = wait(futures, timeout=2, return_when=FIRST_COMPLETED)
            for d in done:
                print(f"Running: {d.running()}, Done: {d.done()}")
                print(d.result())


