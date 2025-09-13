# -*- coding: utf-8 -*-
"""
简化版YOLO训练脚本
支持macOS MPS加速
"""

from ultralytics import YOLO
import torch

def get_device():
    """
    获取最佳可用设备
    优先级：CUDA > MPS > CPU
    """
    if torch.cuda.is_available():
        device = 'cuda'
        print("使用CUDA加速")
    elif torch.backends.mps.is_available():
        device = 'mps'
        print("使用MPS加速 (macOS)")
    else:
        device = 'cpu'
        print("使用CPU")
    
    print(f"设备: {device}")
    return device

def train():
    """简单训练函数"""
    # 获取最佳设备
    device = get_device()
    
    # 加载模型
    model = YOLO('yolov8n.pt')  # 使用完整名称，会自动下载
    
    # 根据设备调整批次大小
    if device == 'mps':
        batch_size = 16  # MPS通常可以处理更大的批次
    elif device == 'cuda':
        batch_size = 8   # 根据显存调整
    else:
        batch_size = 4   # CPU使用较小批次
    
    print(f"批次大小: {batch_size}")
    
    # 检查数据文件路径
    data_path = 'src/utils/yolo/aimlabs/train/images/AimLab Detection.v2i.yolov8/data.yaml'
    import os
    if not os.path.exists(data_path):
        print(f"错误: 找不到数据文件 {data_path}")
        print("请确保在正确的目录运行脚本")
        return None
    
    # 开始训练
    results = model.train(
        data=data_path,
        epochs=50,           # 训练50轮
        imgsz=640,           # 图像大小
        batch=batch_size,    # 批次大小
        device=device,       # 设备
        project='runs',      # 保存路径
        name='aimlab',       # 实验名
        workers=8,           # 增加数据加载线程数
        cache='disk',        # 使用磁盘缓存，避免内存问题
        val=False,           # 跳过验证，加快训练
        plots=False,         # 跳过图表生成
        save_period=10,      # 每10轮保存一次
        patience=20,         # 早停耐心值
        amp=True,            # 自动混合精度
        close_mosaic=10,     # 最后10轮关闭mosaic增强
        nms=False,           # 训练时关闭NMS
    )
    
    print("训练完成!")
    return results

if __name__ == "__main__":
    train()
