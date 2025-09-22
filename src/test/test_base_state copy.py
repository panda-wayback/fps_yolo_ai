from rx.subject import BehaviorSubject
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, Callable, Any, get_type_hints, cast


T = TypeVar('T')

class ReactiveVar(Generic[T]):
    """包装一个可观察的变量"""
    def __init__(self, initial: T = None) -> None:
        self._value: T = initial
        self._subject: BehaviorSubject[T] = BehaviorSubject(initial)

    def set(self, value: T) -> None:
        self._value = value
        self._subject.on_next(value)

    def get(self) -> T:
        return self._value

    def subscribe(self, callback: Callable[[T], None]) -> Any:
        return self._subject.subscribe(callback)

    def __repr__(self) -> str:
        return f"ReactiveVar({self._value})"



class BaseState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        # 获取类型提示
        type_hints = get_type_hints(self.__class__)
        
        # 遍历字段，把普通值替换成 ReactiveVar
        for name, value in self.__dict__.items():
            # 获取字段的类型注解
            field_type = type_hints.get(name, Any)
            # 创建 ReactiveVar 时保持类型信息
            reactive_var = ReactiveVar[field_type](value)
            super().__setattr__(name, reactive_var)

    def __getattribute__(self, name):
        # 获取原始值
        value = super().__getattribute__(name)
        
        # 如果是 ReactiveVar，尝试进行类型转换
        if isinstance(value, ReactiveVar):
            # 获取类型提示
            type_hints = get_type_hints(self.__class__)
            field_type = type_hints.get(name, Any)
            if field_type != Any:
                # 使用 cast 来帮助类型推断，但避免在类型表达式中使用变量
                return cast(Any, value)
        
        return value

    def __setattr__(self, name, value):
        current = self.__dict__.get(name, None)
        if isinstance(current, ReactiveVar):
            current.set(value)  # 更新并通知
        else:
            super().__setattr__(name, value)


# ---------------- 使用 ----------------
class PIDModelState(BaseState):
    kp: ReactiveVar[float] = None
    ki: ReactiveVar[float | None] = None
    kd: ReactiveVar[float | None] = None


pid = PIDModelState()

# 直接在字段上订阅
pid.ki.subscribe(lambda v: print(f"[观察者] ki 更新: {v}"))

# 普通赋值
pid.ki = 0.1
pid.ki = 0.5

print(pid.ki.set())
