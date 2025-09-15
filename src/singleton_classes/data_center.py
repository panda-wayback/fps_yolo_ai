from dataclasses import dataclass, field
from threading import Lock
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor

from singleton_classes.data_state import State


class DataCenter:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.state = State()  # State现在是单例
                    cls._instance._executor = ThreadPoolExecutor(max_workers=4)
        return cls._instance

    def get_state(self) -> State:
        return self.state

    def update_state(self, **kwargs):
        """同步更新状态（阻塞）"""
        for k, v in kwargs.items():
            if hasattr(self.state, k):
                setattr(self.state, k, v)
            else:
                raise KeyError(f"Invalid state key: {k}")

    def update_state_async(self, **kwargs):
        """异步更新状态（返回Future）"""
        def _update():
            with self._lock:
                for k, v in kwargs.items():
                    if hasattr(self.state, k):
                        setattr(self.state, k, v)
                    else:
                        raise KeyError(f"Invalid state key: {k}")
        
        return self._executor.submit(_update)

    async def update_state_task(self, **kwargs):
        """使用asyncio.create_task的异步更新"""
        def _update():
            with self._lock:
                for k, v in kwargs.items():
                    if hasattr(self.state, k):
                        setattr(self.state, k, v)
                    else:
                        raise KeyError(f"Invalid state key: {k}")
        
        # 在线程池中执行
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._executor, _update)

    def create_update_task(self, **kwargs):
        """创建asyncio任务（推荐方式）"""
        def _update():
            with self._lock:
                for k, v in kwargs.items():
                    if hasattr(self.state, k):
                        setattr(self.state, k, v)
                    else:
                        raise KeyError(f"Invalid state key: {k}")
        
        # 创建任务
        loop = asyncio.get_event_loop()
        task = asyncio.create_task(
            loop.run_in_executor(self._executor, _update)
        )
        return task


if __name__ == "__main__":
    dc = DataCenter()
    dc.update_state(test_text="test11")
    print(dc.get_state().test_text)