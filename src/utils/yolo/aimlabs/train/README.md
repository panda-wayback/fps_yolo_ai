# YOLO训练指南

## 数据集信息
- **训练集**: 975张图像
- **验证集**: 278张图像  
- **测试集**: 142张图像
- **类别**: 1个 (targets)
- **格式**: YOLO格式

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 测试MPS加速（可选）
```bash
cd src/utils/yolo/aimlabs/train
python test_mps.py
```

### 3. 修复模型问题（如果遇到下载错误）
```bash
python quick_fix.py
```

### 4. 训练选项
```bash
# 标准训练
python train_simple.py

# 快速训练（跳过验证）
python train_fast.py

# 超快速训练（最小化增强）
python train_ultra_fast.py
```

### 5. 完整训练
```bash
python main.py
```

## 训练参数说明

### 模型选择
- `yolo8n.pt` - 最小最快 (推荐开始)
- `yolo8s.pt` - 小模型
- `yolo8m.pt` - 中等模型
- `yolo8l.pt` - 大模型
- `yolo8x.pt` - 最大最准确

### 设备支持
- **CUDA**: NVIDIA GPU (最快)
- **MPS**: macOS Apple Silicon (M1/M2/M3) - 自动检测
- **CPU**: 备用选项

### 关键参数
- `epochs`: 训练轮数 (建议50-100)
- `batch`: 批次大小 (自动根据设备调整)
  - MPS: 16-32
  - CUDA: 8-16 (根据显存)
  - CPU: 4-8
- `imgsz`: 图像大小 (640推荐)
- `device`: 设备 (自动检测最佳)

## 训练结果
训练完成后，模型会保存在:
- `runs/train/aimlab/weights/best.pt` - 最佳模型
- `runs/train/aimlab/weights/last.pt` - 最后一轮模型

## 使用训练好的模型
```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO('runs/train/aimlab/weights/best.pt')

# 预测
results = model('path/to/image.jpg')
```

## 注意事项
1. **macOS用户**: 自动使用MPS加速，无需额外配置
2. **显存要求**: 
   - MPS: 8GB+ 统一内存 (推荐)
   - CUDA: 4GB+ 显存
   - CPU: 16GB+ 内存
3. 训练时间取决于硬件配置
4. 批次大小自动根据设备调整
5. 建议先用小模型测试，再训练大模型

## MPS加速说明
- 自动检测Apple Silicon芯片
- 使用Metal Performance Shaders
- 比CPU快3-5倍
- 支持M1/M2/M3芯片

## 故障排除

### 问题1: 找不到数据文件
```
FileNotFoundError: 'images/AimLab Detection.v2i.yolov8/data.yaml' does not exist
```
**解决方案**: 使用启动脚本
```bash
python start_training.py
```

### 问题2: 模型下载失败
```
FileNotFoundError: [Errno 2] No such file or directory: 'yolo8n.pt'
```
**解决方案**: 运行修复脚本
```bash
python quick_fix.py
```

### 问题3: MPS不可用
**解决方案**: 检查PyTorch版本和macOS版本
```bash
python test_mps.py
```

### 问题4: 训练速度慢
**解决方案**: 使用快速训练脚本
```bash
# 跳过验证，加快训练
python train_fast.py

# 超快速训练（适合测试）
python train_ultra_fast.py
```

## 速度优化技巧

### 1. **跳过验证**
- 训练时设置 `val=False`
- 验证阶段很耗时，可以跳过

### 2. **增加线程数**
- 设置 `workers=12` 或更高
- 根据CPU核心数调整

### 3. **使用磁盘缓存**
- 设置 `cache='disk'`
- 避免内存不足问题

### 4. **关闭数据增强**
- 减少 `mosaic`, `mixup` 等增强
- 加快数据加载速度

### 5. **减少训练轮数**
- 从50轮减少到20-30轮
- 快速验证模型效果
