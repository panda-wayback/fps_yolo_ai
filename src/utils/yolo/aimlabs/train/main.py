# -*- coding: utf-8 -*-
"""
YOLO训练脚本
用于训练AimLab目标检测模型
"""

import os
import yaml
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

def train_yolo_model():
    """
    训练YOLO模型
    """
    # 获取最佳设备
    device = get_device()
    
    # 数据配置文件路径
    data_yaml_path = "images/AimLab Detection.v2i.yolov8/data.yaml"
    
    # 检查数据文件是否存在
    if not os.path.exists(data_yaml_path):
        print(f"错误: 找不到数据配置文件 {data_yaml_path}")
        return
    
    # 加载YOLO模型 (可以选择不同大小的模型)
    # yolov8n.pt - 最小最快
    # yolov8s.pt - 小
    # yolov8m.pt - 中等
    # yolov8l.pt - 大
    # yolov8x.pt - 最大最准确
    model = YOLO('yolov8n.pt')  # 从预训练模型开始
    
    print("开始训练...")
    
    # 根据设备调整批次大小
    if device == 'mps':
        batch_size = 32  # MPS通常可以处理更大的批次
    elif device == 'cuda':
        batch_size = 16  # 根据显存调整
    else:
        batch_size = 8   # CPU使用较小批次
    
    print(f"批次大小: {batch_size}")
    
    # 训练参数
    results = model.train(
        data=data_yaml_path,           # 数据配置文件
        epochs=100,                    # 训练轮数
        imgsz=640,                     # 输入图像大小
        batch=batch_size,              # 批次大小
        device=device,                 # 使用设备
        project='runs/train',          # 保存路径
        name='aimlab_detection',       # 实验名称
        save=True,                     # 保存模型
        save_period=10,                # 每10轮保存一次
        cache=True,                    # 缓存图像
        workers=4,                     # 数据加载线程数
        patience=20,                   # 早停耐心值
        lr0=0.01,                      # 初始学习率
        lrf=0.01,                      # 最终学习率
        momentum=0.937,                # 动量
        weight_decay=0.0005,           # 权重衰减
        warmup_epochs=3,               # 预热轮数
        warmup_momentum=0.8,           # 预热动量
        warmup_bias_lr=0.1,            # 预热偏置学习率
        box=7.5,                       # 边界框损失权重
        cls=0.5,                       # 分类损失权重
        dfl=1.5,                       # DFL损失权重
        pose=12.0,                     # 姿态损失权重
        kobj=2.0,                      # 关键点对象损失权重
        label_smoothing=0.0,           # 标签平滑
        nbs=64,                        # 标称批次大小
        overlap_mask=True,             # 重叠掩码
        mask_ratio=4,                  # 掩码比率
        drop_path=0.0,                 # Drop path
        val=True,                      # 验证
        plots=True,                    # 生成图表
        verbose=True,                  # 详细输出
    )
    
    print("训练完成!")
    print(f"最佳模型保存在: {results.save_dir}")
    
    return results

def validate_model(model_path):
    """
    验证训练好的模型
    
    Args:
        model_path: 模型文件路径
    """
    model = YOLO(model_path)
    device = get_device()
    
    # 根据设备调整批次大小
    if device == 'mps':
        batch_size = 32
    elif device == 'cuda':
        batch_size = 16
    else:
        batch_size = 8
    
    # 在验证集上测试
    results = model.val(
        data="images/AimLab Detection.v2i.yolov8/data.yaml",
        imgsz=640,
        batch=batch_size,
        conf=0.001,  # 置信度阈值
        iou=0.6,     # IoU阈值
        max_det=300, # 最大检测数
        half=True,   # 半精度
        device=device,
        plots=True,
        save_json=True,
        save_hybrid=True,
    )
    
    print("验证完成!")
    return results

if __name__ == "__main__":
    # 开始训练
    results = train_yolo_model()
    
    # 训练完成后验证
    if results:
        best_model_path = os.path.join(results.save_dir, 'weights', 'best.pt')
        if os.path.exists(best_model_path):
            print(f"\n验证最佳模型: {best_model_path}")
            validate_model(best_model_path)
