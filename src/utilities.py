import time

def elapsed_time_from_function(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    return time.time() - start_time