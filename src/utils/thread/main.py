from concurrent.futures import ThreadPoolExecutor
import atexit
from utils.singleton import singleton

@singleton
class ThreadPoolManager:
    """线程池管理器单例类"""
    
    def __init__(self, max_workers: int = 20, thread_name_prefix: str = "Worker"):
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers, 
            thread_name_prefix=thread_name_prefix
        )
        # 程序退出时自动关闭线程池
        atexit.register(lambda: self.executor.shutdown(wait=True))
    
    def submit(self, func, *args, **kwargs):
        """提交任务到线程池"""
        return self.executor.submit(func, *args, **kwargs)
    
    def get_status(self):
        """获取线程池状态"""
        if self.executor:
            active_threads = len([t for t in self.executor._threads if t.is_alive()])
            pending_tasks = self.executor._work_queue.qsize()
            
            return {
                "max_workers": self.executor._max_workers,
                "active_threads": active_threads,
                "pending_tasks": pending_tasks,
                "utilization": f"{active_threads}/{self.executor._max_workers} ({active_threads/self.executor._max_workers*100:.1f}%)",
                "queue_size": pending_tasks
            }
        return None

# 全局单例实例
_thread_pool_manager = ThreadPoolManager()

def get_thread_pool():
    """获取线程池管理器单例"""
    return _thread_pool_manager

# 便捷的装饰器和函数
def threaded(func):
    """
    使用线程池执行函数的装饰器（自动提交，不返回Future）
    
    用法:
        @threaded
        def my_task(value):
            print(value)
        
        my_task("Hello")  # 自动在线程池中执行
    """
    def wrapper(*args, **kwargs):
        _thread_pool_manager.submit(func, *args, **kwargs)
    return wrapper

def threaded_return(func):
    """
    使用线程池执行函数的装饰器（返回Future对象）
    
    用法:
        @threaded_return
        def my_task(value):
            return value * 2
        
        future = my_task("Hello")  # 返回Future
        result = future.result()   # 获取结果
    """
    def wrapper(*args, **kwargs):
        return _thread_pool_manager.submit(func, *args, **kwargs)
    return wrapper

def submit_task(func, *args, **kwargs):
    """
    直接提交任务到线程池（用于动态调用）
    
    用法:
        submit_task(my_function, arg1, arg2, key=value)
    """
    return _thread_pool_manager.submit(func, *args, **kwargs)

def get_pool_status():
    """获取线程池状态"""
    return _thread_pool_manager.get_status()

def print_pool_status():
    """打印线程池状态"""
    status = get_pool_status()
    if status:
        print(f"🧵 线程池状态: {status['utilization']}, 队列: {status['queue_size']}")
    else:
        print("🧵 线程池未初始化")

if __name__ == "__main__":
    import time
    
    print("=== ThreadPoolManager 测试 ===\n")
    
    # 测试1: 基本装饰器（不返回结果）
    print("📝 测试1: @threaded 装饰器（自动提交）")
    @threaded
    def task1(value):
        time.sleep(0.1)
        print(f"  ✅ 任务1完成: {value}")
    
    task1("Hello")
    threaded(task1("Hello2"))
    print_pool_status()
    
    # 测试2: 返回Future的装饰器
    print("\n📝 测试2: @threaded_return 装饰器（返回Future）")
    @threaded_return
    def task2(name, age):
        time.sleep(0.1)
        return f"{name}, {age}岁"
    
    future = task2("张三", 25)
    print(f"  ✅ 任务2结果: {future.result()}")
    
    # 测试3: 动态提交任务
    print("\n📝 测试3: submit_task 动态提交")
    def task3(x, y):
        time.sleep(0.1)
        return x + y
    
    future = submit_task(task3, x=10, y=20)
    print(f"  ✅ 任务3结果: {future.result()}")
    
    # 最终状态
    print("\n🧵 最终线程池状态:")
    print_pool_status()