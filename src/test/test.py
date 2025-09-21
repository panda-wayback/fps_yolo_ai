from rx.subject import BehaviorSubject
from pydantic import BaseModel, ConfigDict


class ReactiveVar:
    """包装一个可观察的变量"""
    def __init__(self, initial=None):
        self._value = initial
        self._subject = BehaviorSubject(initial)

    def set(self, value):
        self._value = value
        self._subject.on_next(value)

    def get(self):
        return self._value

    def subscribe(self, callback):
        return self._subject.subscribe(callback)

    def __repr__(self):
        return f"ReactiveVar({self._value})"


class ReactiveVarWrapper:
    """包装器，让 ReactiveVar 在打印时显示值，但保留所有方法"""
    def __init__(self, reactive_var):
        self._reactive_var = reactive_var

    def __getattr__(self, name):
        """代理所有方法调用到原始的 ReactiveVar"""
        return getattr(self._reactive_var, name)

    def __repr__(self):
        """打印时显示实际值"""
        return repr(self._reactive_var.get())

    def __str__(self):
        """字符串转换时显示实际值"""
        return str(self._reactive_var.get())


class BaseState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        # 遍历字段，把普通值替换成 ReactiveVar
        for name, value in self.__dict__.items():
            super().__setattr__(name, ReactiveVar(value))

    def __setattr__(self, name, value):
        current = self.__dict__.get(name, None)
        if isinstance(current, ReactiveVar):
            current.set(value)  # 更新并通知
        else:
            super().__setattr__(name, value)
    
    def __getattribute__(self, name):
        """重写属性访问，让 ReactiveVar 对象直接返回值"""
        value = super().__getattribute__(name)
        if isinstance(value, ReactiveVar):
            # 如果访问的是 ReactiveVar 对象，返回一个包装器
            return ReactiveVarWrapper(value)
        return value


# ---------------- 使用 ----------------
class PIDModelState(BaseState):
    kp: float | None = None
    ki: float | None = None
    kd: float | None = None


pid = PIDModelState()

# 直接在字段上订阅
pid.ki.subscribe(lambda v: print(f"[观察者] ki 更新: {v}"))

# 普通赋值
pid.ki = 0.1
pid.ki = 0.5

print(pid.ki)