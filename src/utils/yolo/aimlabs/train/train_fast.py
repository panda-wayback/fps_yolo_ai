# -*- coding: utf-8 -*-
"""
快速训练脚本
优化训练速度，减少验证频率
"""

from ultralytics import YOLO
import torch

def get_device():
    """获取最佳可用设备"""
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

def train_fast():
    """快速训练函数"""
    # 获取最佳设备
    device = get_device()
    
    # 加载模型
    model = YOLO('yolov8n.pt')
    
    # 根据设备调整参数
    if device == 'mps':
        batch_size = 32  # 增加批次大小
    elif device == 'cuda':
        batch_size = 16
    else:
        batch_size = 8
    
    print(f"批次大小: {batch_size}")
    
    # 检查数据文件
    data_path = 'src/utils/yolo/aimlabs/train/images/AimLab Detection.v2i.yolov8/data.yaml'
    import os
    if not os.path.exists(data_path):
        print(f"错误: 找不到数据文件 {data_path}")
        return None
    
    # 快速训练参数
    results = model.train(
        data=data_path,
        epochs=30,           # 减少训练轮数
        imgsz=640,           # 图像大小
        batch=batch_size,    # 批次大小
        device=device,       # 设备
        project='runs',      # 保存路径
        name='aimlab_fast',  # 实验名
        workers=12,          # 增加线程数
        cache='disk',        # 磁盘缓存
        val=False,           # 跳过验证
        plots=False,         # 跳过图表
        save_period=5,       # 每5轮保存
        patience=15,         # 早停
        amp=True,            # 混合精度
        close_mosaic=5,      # 最后5轮关闭mosaic
        nms=False,           # 关闭NMS
        verbose=True,        # 详细输出
        # 优化参数
        lr0=0.01,           # 学习率
        lrf=0.01,           # 最终学习率
        momentum=0.937,      # 动量
        weight_decay=0.0005, # 权重衰减
        warmup_epochs=3,     # 预热轮数
        # 数据增强优化
        hsv_h=0.015,        # 色调变化
        hsv_s=0.7,          # 饱和度变化
        hsv_v=0.4,          # 明度变化
        degrees=0.0,         # 旋转角度
        translate=0.1,       # 平移
        scale=0.5,           # 缩放
        shear=0.0,           # 剪切
        perspective=0.0,     # 透视变换
        flipud=0.0,          # 上下翻转
        fliplr=0.5,          # 左右翻转
        mosaic=1.0,          # Mosaic增强
        mixup=0.0,           # Mixup增强
        copy_paste=0.0,      # 复制粘贴增强
    )
    
    print("快速训练完成!")
    return results

if __name__ == "__main__":
    train_fast()
