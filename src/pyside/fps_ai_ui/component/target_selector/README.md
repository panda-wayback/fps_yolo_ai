# 目标选择器UI组件

目标选择器的用户界面组件，提供配置和状态显示功能。

## 组件结构

```
target_selector/
├── component/
│   ├── target_selector_config.py    # 配置组件
│   └── target_selector_state.py     # 状态显示组件
└── index.py                         # 主入口
```

## 功能特性

### 配置组件 (target_selector_config.py)
- **权重滑块**: 距离权重、置信度权重、相似度权重、类别权重
- **参考向量设置**: X、Y坐标输入
- **实时配置**: 滑块变化时实时更新
- **应用配置**: 手动应用配置到系统
- **重置功能**: 恢复默认值
- **状态提示**: 显示配置保存状态

### 状态显示组件 (target_selector_state.py)
- **目标信息**: 显示选中目标的详细信息
- **实时更新**: 每100ms自动刷新状态
- **配置显示**: 显示当前生效的配置参数
- **状态指示**: 颜色编码的状态显示

## 使用方法

### 基本使用

```python
from pyside.fps_ai_ui.component.target_selector.index import create_target_selector_component

# 创建完整的目标选择器组件
widget = create_target_selector_component()
```

### 单独使用配置组件

```python
from pyside.fps_ai_ui.component.target_selector.component.target_selector_config import create_target_selector_config

# 只创建配置组件
config_widget = create_target_selector_config()
```

### 单独使用状态组件

```python
from pyside.fps_ai_ui.component.target_selector.component.target_selector_state import create_target_selector_state

# 只创建状态显示组件
state_widget = create_target_selector_state()
```

## 界面说明

### 配置界面
- **距离权重滑块**: 控制目标距离屏幕中心的权重 (0.0-1.0)
- **置信度权重滑块**: 控制YOLO检测置信度的权重 (0.0-1.0)
- **相似度权重滑块**: 控制与参考向量相似度的权重 (0.0-1.0)
- **类别权重滑块**: 控制特定类别的权重 (0.0-1.0)
- **参考向量**: 设置用于相似度计算的参考点坐标
- **重置默认值按钮**: 将所有参数恢复为默认值
- **应用配置按钮**: 将当前设置应用到系统

### 状态界面
- **选中状态**: 显示是否已选中目标（绿色=已选中，红色=未选中）
- **中心点**: 显示选中目标的中心坐标
- **边界框**: 显示目标的边界框坐标 (x1, y1, x2, y2)
- **置信度**: 显示目标的检测置信度（带进度条）
- **类别ID**: 显示目标的类别标识
- **当前配置**: 显示所有权重参数的当前值
- **更新时间**: 显示最后更新时间

## 集成到主界面

```python
# 在主界面中添加目标选择器组件
from pyside.fps_ai_ui.component.target_selector.index import create_target_selector_component

def create_main_window():
    # ... 其他组件 ...
    
    # 添加目标选择器
    target_selector = create_target_selector_component()
    layout.addWidget(target_selector)
    
    # ... 其他代码 ...
```

## 注意事项

1. **实时更新**: 状态组件会自动更新，无需手动刷新
2. **配置持久化**: 配置更改会立即应用到数据中心的state中
3. **错误处理**: 组件包含完整的错误处理和状态提示
4. **性能优化**: 状态更新间隔为100ms，平衡了响应性和性能
