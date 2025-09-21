from pydantic import BaseModel, ConfigDict
from rx.subject import BehaviorSubject


class ReactiveVar:
    """包装一个可观察的变量"""
    def __init__(self, initial=None):
        self._value = initial
        self._subject = BehaviorSubject(initial)
        self._initialized = False  # 标记是否已经初始化

    def set(self, value):
        # 只有当值真正发生变化时才触发通知
        if self._value != value:
            self._value = value
            self._subject.on_next(value)
        # 标记为已初始化
        self._initialized = True

    def get(self):
        return self._value

    def subscribe(self, callback):
        return self._subject.subscribe(callback)

    def __repr__(self):
        return f"ReactiveVar({self._value})"
    
    def __deepcopy__(self, memo):
        """自定义深拷贝，避免 BehaviorSubject 的序列化问题"""
        # 创建一个新的 ReactiveVar 实例，只复制值，不复制 subject
        new_instance = ReactiveVar(self._value)
        return new_instance
    
    def __getstate__(self):
        """序列化时只保存值，不保存 subject"""
        return {'_value': self._value}
    
    def __setstate__(self, state):
        """反序列化时重建 subject"""
        self._value = state['_value']
        self._subject = BehaviorSubject(self._value)


class BaseState(BaseModel):
    """状态管理基类，提供响应式状态管理和通用的更新方法"""
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
    
    def update_state(self, **kwargs):
        """更新状态，只更新提供的字段，保持其他字段不变"""
        for key, value in kwargs.items():
            if key in self.model_fields:
                setattr(self, key, value)
    
    def merge_state(self, other_state: 'BaseState'):
        """合并另一个状态对象，other_state的字段优先"""
        if other_state is not None:
            # 只合并非None的字段
            update_data = {}
            for key, value in other_state.model_dump().items():
                if value is not None:
                    update_data[key] = value
            self.update_state(**update_data)