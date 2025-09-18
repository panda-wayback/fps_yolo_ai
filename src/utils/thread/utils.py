import time
import threading
import numpy as np

# 封装线程执行器
def threaded(func):
    def wrapper(value):
        t = threading.Thread(target=func, args=(value,))
        t.daemon = True
        t.start()
    return wrapper

def threaded_with_args(func, *args, **kwargs):
    import threading
    time.sleep(1)
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    return t