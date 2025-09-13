# FPS游戏AI辅助系统使用指南

## 系统概述

这是一个完整的FPS游戏AI辅助系统，集成了：
- **YOLO目标检测** - 自动识别游戏中的目标
- **PID控制器** - 精确控制准星移动
- **鼠标控制** - 自动移动鼠标到目标位置

## 文件结构

```
src/
├── main.py                    # 主程序入口
├── test_model.py             # 模型测试程序
├── utils/
│   ├── pid/
│   │   └── pid.py           # PID控制器
│   ├── move_mouse/
│   │   └── move_mouse.py    # 鼠标控制
│   ├── screenshot_tool/
│   │   └── mss_screenshot.py # 屏幕截图
│   └── yolo/
│       └── aimlabs/train/   # YOLO训练相关
runs/
└── aimlab_fast/
    └── weights/
        └── best.pt          # 训练好的模型
```

## 使用步骤

### 1. 测试模型

首先测试训练好的模型是否正常工作：

```bash
cd src
python test_model.py
```

这会：
- 加载训练好的模型
- 创建测试图像
- 进行目标检测
- 保存检测结果

### 2. 运行主程序

```bash
cd src
python main.py
```

### 3. 系统功能

#### 自动目标检测
- 实时截取屏幕
- 使用YOLO模型检测目标
- 选择置信度最高的目标

#### 智能准星控制
- 计算准星到目标的误差向量
- 使用PID控制器计算移动量
- 平滑移动鼠标到目标位置

#### 高频率更新
- 默认50Hz更新频率
- 每20ms更新一次
- 确保快速响应

## 配置选项

### PID控制器预设

在 `main.py` 中可以调整PID控制器：

```python
# 创建AI辅助系统
ai_assistant = FPSAIAssistant()

# 更新PID设置
ai_assistant.update_pid_settings("balanced")  # 平衡模式
ai_assistant.update_pid_settings("aggressive")  # 激进模式
ai_assistant.update_pid_settings("precise")    # 精确模式
ai_assistant.update_pid_settings("smooth")     # 平滑模式
```

### 运行频率

```python
# 调整更新频率
ai_assistant.run(fps=50)  # 50Hz
ai_assistant.run(fps=60)  # 60Hz
ai_assistant.run(fps=30)  # 30Hz
```

### 置信度阈值

在 `main.py` 中调整检测置信度：

```python
# 在 detect_targets 方法中
if conf > 0.5:  # 调整这个阈值
    targets.append({...})
```

## 性能优化

### 设备选择
系统会自动选择最佳计算设备：
- **MPS** - macOS Apple Silicon (M1/M2/M3)
- **CUDA** - NVIDIA GPU
- **CPU** - 备用选项

### 模型优化
- 使用训练好的 `best.pt` 模型
- 支持MPS加速（macOS）
- 自动设备检测

## 故障排除

### 常见问题

1. **模型文件不存在**
   ```
   ❌ 错误: 找不到模型文件 runs/aimlab_fast/weights/best.pt
   ```
   **解决方案**: 确保模型文件存在，或重新训练模型

2. **截图失败**
   ```
   ❌ 截图失败
   ```
   **解决方案**: 检查屏幕权限，确保程序有屏幕录制权限

3. **鼠标移动无效**
   ```
   ❌ 鼠标移动失败
   ```
   **解决方案**: 检查辅助功能权限，确保程序有控制鼠标的权限

### 权限设置

#### macOS
1. **屏幕录制权限**:
   - 系统偏好设置 → 安全性与隐私 → 隐私 → 屏幕录制
   - 添加Python或终端应用

2. **辅助功能权限**:
   - 系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能
   - 添加Python或终端应用

## 安全提醒

⚠️ **重要提醒**:
- 本系统仅用于学习和研究目的
- 请遵守游戏服务条款
- 不要在多人在线游戏中使用
- 建议仅在单机游戏或训练模式中使用

## 技术细节

### PID控制器
- 使用纯比例控制(P控制器)
- 高响应，无累积误差
- 支持动态参数调整

### 目标检测
- 基于YOLOv8模型
- 支持实时检测
- 自动选择最佳目标

### 鼠标控制
- 高精度移动
- 支持浮点数坐标
- 平滑移动轨迹

## 开发信息

- **Python版本**: 3.8+
- **主要依赖**: ultralytics, opencv-python, pynput, mss
- **支持平台**: macOS, Windows, Linux
- **硬件要求**: 8GB+ 内存，支持MPS/CUDA更佳
