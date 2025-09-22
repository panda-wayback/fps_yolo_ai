from rx.subject import BehaviorSubject
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, Callable, Any
import copy

T = TypeVar('T')


class ReactiveVar(Generic[T]):
    """包装一个可观察的变量"""
    def __init__(self, initial: T = None) -> None:
        self._value: T = initial
        self._subject: BehaviorSubject[T] = BehaviorSubject(initial)

    def set(self, value: T) -> None:
        if self._value != value:  # 避免重复通知
            self._value = value
            self._subject.on_next(value)

    def get(self) -> T:
        return self._value

    def subscribe(self, callback: Callable[[T], None]) -> Any:
        return self._subject.subscribe(callback)

    def __repr__(self) -> str:
        return f"ReactiveVar({self._value!r})"

    def __deepcopy__(self, memo):
        return ReactiveVar(copy.deepcopy(self._value, memo))


class BaseState(BaseModel):
    """自动将字段包装成 ReactiveVar 的状态模型"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        for name, value in self.__dict__.items():
            if not isinstance(value, ReactiveVar):
                super().__setattr__(name, ReactiveVar(value))

    def __setattr__(self, name, value):
        current = self.__dict__.get(name)
        if isinstance(current, ReactiveVar):
            current.set(value)  # 更新并触发通知
        else:
            super().__setattr__(name, value)

    def to_dict(self) -> dict:
        """导出干净的 dict（递归展开 ReactiveVar 和 BaseState）"""
        result = {}
        for name, value in self.__dict__.items():
            if isinstance(value, ReactiveVar):
                val = value.get()
                if isinstance(val, BaseState):
                    result[name] = val.to_dict()
                else:
                    result[name] = val
            elif isinstance(value, BaseState):
                result[name] = value.to_dict()
            else:
                result[name] = value
        return result

    def __deepcopy__(self, memo):
        """深拷贝：复制值，但生成独立的 ReactiveVar"""
        data = self.to_dict()
        return self.__class__(**copy.deepcopy(data, memo))

