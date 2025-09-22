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
        # 只有当值真正发生变化时才更新并通知
        if self._value != value:
            self._value = value
            self._subject.on_next(value)

    def get(self) -> T:
        return self._value

    def subscribe(self, callback: Callable[[T], None]) -> Any:
        return self._subject.subscribe(callback)

    def __repr__(self) -> str:
        return f"ReactiveVar({self._value})"
    
    def __deepcopy__(self, memo):
        """支持深拷贝操作，创建新的 ReactiveVar 实例"""
        # 创建一个新的 ReactiveVar 实例，只复制值，不复制 BehaviorSubject
        new_instance = ReactiveVar(self._value)
        return new_instance



class BaseState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        # 遍历字段，把普通值替换成 ReactiveVar
        for name, value in self.__dict__.items():
            # 获取字段的类型注解
            field_type = self.__annotations__.get(name, Any)
            # 创建 ReactiveVar 时保持类型信息
            reactive_var = ReactiveVar[field_type](value)
            super().__setattr__(name, reactive_var)

    def __setattr__(self, name, value):
        current = self.__dict__.get(name, None)
        if isinstance(current, ReactiveVar):
            current.set(value)  # 更新并通知
        else:
            super().__setattr__(name, value)
    
    def __deepcopy__(self, memo):
        """支持深拷贝操作"""
        # 创建一个新的实例
        new_instance = self.__class__()
        
        # 复制所有字段的值（不是 ReactiveVar 对象）
        for name, value in self.__dict__.items():
            if isinstance(value, ReactiveVar):
                # 对于 ReactiveVar，只复制其值
                new_instance.__setattr__(name, value.get())
            else:
                new_instance.__setattr__(name, value)
        
        return new_instance

