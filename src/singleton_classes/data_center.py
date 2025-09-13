from dataclasses import dataclass, field
from threading import Lock
import numpy as np

from singleton_classes.data_state import State


class DataCenter:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.state = State()
        return cls._instance

    def get_state(self) -> State:
        return self.state

    def update_state(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self.state, k):
                setattr(self.state, k, v)
            else:
                raise KeyError(f"Invalid state key: {k}")


if __name__ == "__main__":
    dc = DataCenter()
    dc.update_state(test_text="test11")
    print(dc.get_state().test_text)