"""
FPS游戏AI辅助主程序 - 最小示例
加载YOLO模型并检测鼠标周围的目标
"""

import sys
import os
import torch

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultralytics import YOLO


def get_device():
    """获取最佳计算设备"""
    if torch.backends.mps.is_available():
        return 'mps'
    elif torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'

def get_aimlabs_model():
    """主函数 - 最小示例"""
    print("=== FPS AI辅助系统 - 最小示例 ===")
    
    # 获取计算设备
    device = get_device()
    print(f"使用设备: {device}")
    
    # 1. 加载YOLO模型
    model_path = "runs/aimlab_fast/weights/best.pt"
    print(f"正在加载模型: {model_path}")
    
    try:
        model = YOLO(model_path)
        model.to(device)
        print("✅ 模型加载成功")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return
    return model

if __name__ == "__main__":
    get_aimlabs_model()
