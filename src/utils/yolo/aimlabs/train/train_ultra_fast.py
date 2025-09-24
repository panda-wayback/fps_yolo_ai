# -*- coding: utf-8 -*-
"""
超快速训练脚本
最小化验证，最大化训练速度
"""

from ultralytics import YOLO
import torch

def train_ultra_fast():
    """超快速训练"""
    device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"使用设备: {device}")
    
    model = YOLO('yolov8n.pt')
    
    # 超快速训练参数
    results = model.train(
        data='src/utils/yolo/aimlabs/train/images/AimLab Detection.v2i.yolov8/data.yaml',
        epochs=20,           # 只训练20轮
        imgsz=640,
        batch=32,            # 大批次
        device=device,
        project='runs',
        name='aimlab_ultra_fast',
        workers=16,          # 最大线程数
        cache='disk',
        val=False,           # 完全跳过验证
        plots=False,
        save_period=10,      # 只保存最终模型
        patience=10,
        amp=True,
        nms=False,
        verbose=False,       # 减少输出
        # 最小化数据增强
        mosaic=0.0,          # 关闭mosaic
        mixup=0.0,           # 关闭mixup
        copy_paste=0.0,      # 关闭copy_paste
        degrees=0.0,         # 关闭旋转
        translate=0.0,       # 关闭平移
        scale=0.0,           # 关闭缩放
        shear=0.0,           # 关闭剪切
        perspective=0.0,     # 关闭透视
        flipud=0.0,          # 关闭上下翻转
        fliplr=0.0,          # 关闭左右翻转
        hsv_h=0.0,           # 关闭色调变化
        hsv_s=0.0,           # 关闭饱和度变化
        hsv_v=0.0,           # 关闭明度变化
    )
    
    print("超快速训练完成!")
    return results

if __name__ == "__main__":
    train_ultra_fast()
