import time
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import atexit

# 简单的全局线程池
_executor = None

def get_executor():
    """获取全局线程池"""
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=20, thread_name_prefix="Worker")
        # 程序退出时自动关闭线程池
        atexit.register(lambda: _executor.shutdown(wait=True))
    return _executor

# 封装线程执行器 - 使用简单线程池
def threaded(func):
    """使用线程池执行函数"""
    def wrapper(value):
        get_executor().submit(func, value)
    return wrapper

def threaded_with_args(func, *args, **kwargs):
    """使用线程池执行带参数的函数"""
    return get_executor().submit(func, *args, **kwargs)

def get_pool_status():
    """获取线程池状态"""
    global _executor
    if _executor:
        active_threads = len([t for t in _executor._threads if t.is_alive()])
        pending_tasks = _executor._work_queue.qsize()
        
        return {
            "max_workers": _executor._max_workers,
            "active_threads": active_threads,
            "pending_tasks": pending_tasks,
            "utilization": f"{active_threads}/{_executor._max_workers} ({active_threads/_executor._max_workers*100:.1f}%)",
            "queue_size": pending_tasks
        }
    return None

def print_pool_status():
    """打印线程池状态"""
    status = get_pool_status()
    if status:
        print(f"🧵 线程池状态: {status['utilization']}, 队列: {status['queue_size']}")
    else:
        print("🧵 线程池未初始化")