import multiprocessing as mp
from multiprocessing import Process
from multiprocessing import Queue
from time import time


'''Numerically calculates the derivative of a function
by means of tiny increments'''
def differentiate(function, point, sub):
    diff = 1 / sub
    return (function(point + diff) - function(point)) / diff


def integrate(function, bounds, sub, passes_log=False, cores=2):

    cores //= 2
    down, up = bounds
    dx = (up - down) / sub
    aprox = 0.0

    def partial_upper(portion, queue):
        psub = sub // cores
        aprox = 0.0
        for j in range(portion * psub, (portion + 1) * psub):
            x = down + j * dx
            area = function(x) * dx
            aprox += area
            if portion == 3 and passes_log:
                current_pass = str((portion + 1) * psub - j)
                backspaces = "".join(["\b"] * (len(current_pass) + 13))
                print(f"Passes left: {current_pass}", end="", flush=True)
                print(backspaces, end="")
        queue.put(aprox)

    def partial_lower(portion, queue):
        psub = sub // cores
        aprox = 0.0
        for j in range(portion * psub + 1, (portion + 1) * psub + 1):
            x = down + j * dx
            area = function(x) * dx
            aprox += area
        queue.put(aprox)

    def upper(queue):
        aprox = 0.0
        q = Queue()
        processes = [Process(target=partial_upper, args=(c, q)) for c in range(cores)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
            aprox += q.get()
        queue.put(aprox)

    def lower(queue):
        aprox = 0.0
        q = Queue()
        processes = [Process(target=partial_lower, args=(c, q)) for c in range(cores)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
            aprox += q.get()
        queue.put(aprox)

    q = Queue()

    u = Process(target=upper, args=(q,))
    u.start()

    l = Process(target=lower, args=(q,))
    l.start()

    u.join()
    aprox += q.get()

    l.join()
    aprox += q.get()

    if passes_log:
        print("Done!")

    return aprox / 2


if __name__ == "__main__":

    '''Lets numerically calculate the value
    of pi with the magic of multiprocessing!'''

    import numpy as np

    f = lambda x : np.arccosh(x) / x if x != 0.0 else 1
    b = -10000, 10000
    p = 1000000
    ti = time()
    result = integrate(f, b, p, False, cores=8)
    tf = time()
    print(f"Running time: {tf - ti:.3f}s")
    print(f"Expected value: {np.pi * 0.5}")
    print(f"Computed value: {result}")
    print(f"Relative error: {abs(1 - (result / (np.pi * 0.5)))*100}%")
