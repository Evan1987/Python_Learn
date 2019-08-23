
"""
python因为其全局解释器锁GIL而无法通过线程实现真正的平行计算。这个论断我们不展开，但是有个概念我们要说明，IO密集型 vs. 计算密集型。
    IO密集型：读取文件，读取网络套接字频繁。
    计算密集型：大量消耗CPU的数学与逻辑运算，也就是我们这里说的平行计算。
而concurrent.futures模块，可以利用multiprocessing实现真正的平行计算。
核心原理是：concurrent.futures会以子进程的形式，平行的运行多个python解释器，从而令python程序可以利用多核CPU来提升执行速度。
由于子进程与主解释器相分离，所以他们的全局解释器锁也是相互独立的。每个子进程都能够完整的使用一个CPU内核。
source: https://www.cnblogs.com/kangoroo/p/7628092.html
"""
import _utils.context as _context
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


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


if __name__ == '__main__':
    with _context.timer(name="Single Thread"):  # 0.4558
        result = list(map(gcd, numbers))

    with _context.timer(name="Multi Thread"):  # 0.4019
        with ThreadPoolExecutor(max_workers=2) as pool:
            result = list(pool.map(gcd, numbers))

    with _context.timer(name="Multi Process"):  # 0.3790
        with ProcessPoolExecutor(max_workers=2) as pool:
            result = list(pool.map(gcd, numbers))

# 多进程操作流程
# 1）把numbers列表中的每一项输入数据都传给map。
# 2）用pickle模块对数据进行序列化，将其变成二进制形式。
# 3）通过本地套接字，将序列化之后的数据从煮解释器所在的进程，发送到子解释器所在的进程。
# 4）在子进程中，用pickle对二进制数据进行反序列化，将其还原成python对象。
# 5）引入包含gcd函数的python模块。
# 6）各个子进程并行的对各自的输入数据进行计算。
# 7）对运行的结果进行序列化操作，将其转变成字节。
# 8）将这些字节通过socket复制到主进程之中。
# 9）主进程对这些字节执行反序列化操作，将其还原成python对象。
# 10）最后，把每个子进程所求出的计算结果合并到一份列表之中，并返回给调用者。
# multiprocessing开销比较大，原因就在于：主进程和子进程之间通信，必须进行序列化和反序列化的操作。
