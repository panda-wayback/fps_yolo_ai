from rx.subject import BehaviorSubject
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, Callable, Any


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


# ---------------- 使用 ----------------
class PIDModelState(BaseState):
    kp: ReactiveVar[float| None] = 0.5
    ki: ReactiveVar[float | None] = None
    kd: ReactiveVar[float | None] = None


pid = PIDModelState()

# 直接在字段上订阅
pid.ki.subscribe(lambda v: print(f"[观察者] ki 更新: {v}"))

# 普通赋值
pid.ki = 0.1
pid.ki = 0.5

# 测试相同值不会触发通知
print("--- 测试相同值 ---")
pid.ki = 0.5  # 相同值，不应该触发通知
pid.ki = 0.5  # 再次相同值，不应该触发通知
pid.ki = 0.5  # 第三次相同值，不应该触发通知

print(f"当前 ki 值: {pid.ki.get()}")

# 只有真正变化时才触发
print("--- 测试值变化 ---")
pid.ki = 0.3  # 不同值，应该触发通知
pid.ki = 0.3  # 相同值，不应该触发通知
