import time


def benchmark(func: callable):
    def function_timer(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        runtime = end - start
        message = f"[{func.__name__}] took {runtime * 1000:.2f} ms"
        print(message)
        return value

    return function_timer