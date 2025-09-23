# PID控制器组件

PID控制器组件提供了完整的PID参数配置和状态监控功能。

## 功能特性

### 配置功能
- **Kp参数调节**：比例增益，范围 0.0-10.0
- **Ki参数调节**：积分增益，范围 0.0-5.0  
- **Kd参数调节**：微分增益，范围 0.0-5.0
- **采样时间设置**：控制周期，范围 0.001-0.1秒
- **实时参数应用**：参数修改后立即生效
- **参数重置**：一键恢复默认值
- **参数保存**：保存当前配置

### 状态监控
- **实时参数显示**：显示当前Kp、Ki、Kd、采样时间
- **输出监控**：实时显示X轴和Y轴输出值
- **控制状态**：显示PID控制器是否启用
- **输出强度条**：可视化显示输出强度
- **控制日志**：记录控制过程和错误信息

## 组件结构

```
pid_controller/
├── component/
│   ├── pid_config.py      # PID参数配置组件
│   └── pid_state.py       # PID状态监控组件
├── index.py               # 主入口文件
└── README.md              # 说明文档
```

## 使用方法

### 基本使用

```python
from pyside.fps_ai_ui.component.pid_controller.index import get_pid_controller_component

# 创建完整的PID控制器组件
pid_component = get_pid_controller_component()

# 或者分别创建配置和状态组件
from pyside.fps_ai_ui.component.pid_controller.component.pid_config import create_pid_config
from pyside.fps_ai_ui.component.pid_controller.component.pid_state import create_pid_state

config_widget = create_pid_config()
state_widget = create_pid_state()
```

### 参数调节

1. **使用滑块调节**：拖动滑块可以实时调节参数值
2. **查看数值**：滑块右侧显示当前参数值
3. **应用设置**：点击"应用"按钮使参数生效
4. **重置参数**：点击"重置"按钮恢复默认值

### 状态监控

- **实时更新**：状态显示每100ms自动更新
- **参数显示**：显示当前生效的PID参数
- **输出监控**：实时显示X轴和Y轴输出
- **状态指示**：绿色表示已启用，红色表示未启用
- **日志查看**：查看控制过程中的日志信息

## 参数说明

### PID参数
- **Kp (比例增益)**：控制响应速度，值越大响应越快
- **Ki (积分增益)**：消除稳态误差，值越大消除越快
- **Kd (微分增益)**：减少超调，值越大超调越小
- **采样时间**：控制周期，影响控制精度和响应速度

### 默认值
- Kp: 1.0
- Ki: 0.1  
- Kd: 0.1
- 采样时间: 0.02s

## 注意事项

1. **参数范围**：请确保参数在合理范围内，避免系统不稳定
2. **实时应用**：参数修改后需要点击"应用"才能生效
3. **状态监控**：状态显示会实时更新，反映当前PID控制器状态
4. **日志管理**：日志会自动限制在50行以内，避免内存占用过多

## 集成说明

该组件与以下模块集成：
- `data_center.models.pid_model`：PID模型状态管理
- `singleton_classes.pid_controller`：PID控制器实现
- `data_center.models.mouse_driver_model`：鼠标驱动控制

## 测试

运行 `index.py` 可以独立测试PID控制器组件：

```bash
python src/pyside/fps_ai_ui/component/pid_controller/index.py
```
