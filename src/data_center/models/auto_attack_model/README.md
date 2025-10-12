# 自动攻击模型模块

## 📁 文件结构

```
auto_attack_model/
├── __init__.py                    # 模块初始化
├── model.py                       # 数据模型定义
├── state.py                       # 状态管理
├── subject.py                     # 主题/接口
├── subscribes/                    # 订阅者文件夹
│   ├── __init__.py
│   └── example_subscribe.py       # 示例订阅者（可删除）
└── README.md                      # 本文件
```

## 🎯 模块说明

### `model.py` - 数据模型
定义自动攻击相关的状态数据，使用 `ReactiveVar` 实现响应式更新。

```python
from data_center.models.auto_attack_model.model import AutoAttackModel

# 默认值在这里定义
AutoAttackModel.is_enabled  # 默认 False
```

### `state.py` - 状态管理
提供状态实例的获取接口。

```python
from data_center.models.auto_attack_model.state import AutoAttackModelState

# 获取状态实例
state = AutoAttackModelState.get_state()
```

### `subject.py` - 主题接口
对外提供的统一接口，用于操作状态。

```python
from data_center.models.auto_attack_model.subject import AutoAttackSubject

# 使用接口
AutoAttackSubject.enable()   # 启用
AutoAttackSubject.disable()  # 禁用
AutoAttackSubject.toggle()   # 切换
```

### `subscribes/` - 订阅者
存放订阅状态变化的处理函数。

## 💡 使用示例

```python
# 1. 导入模块
from data_center.models.auto_attack_model.subject import AutoAttackSubject
from data_center.models.auto_attack_model.state import AutoAttackModelState

# 2. 修改状态
AutoAttackSubject.enable()

# 3. 读取状态
is_enabled = AutoAttackModelState.get_state().is_enabled.get()
print(f"自动攻击: {is_enabled}")
```

## 🔧 TODO

在以下位置添加你自己的内容：

1. **model.py**
   - 添加需要的状态字段
   - 添加攻击参数
   - 添加统计信息

2. **subject.py**
   - 添加更多方法
   - 实现业务逻辑

3. **subscribes/**
   - 添加订阅者文件
   - 实现状态监听

## 📚 参考其他模块

可以参考以下模块的实现：
- `controller_model` - 控制器模型
- `yolo_model` - YOLO 模型
- `target_selector` - 目标选择器

