# -*- coding: utf-8 -*-
"""
MPS加速测试脚本
测试macOS上的MPS加速是否正常工作
"""

import torch
from ultralytics import YOLO

def test_mps():
    """测试MPS加速"""
    print("=== MPS加速测试 ===")
    
    # 检查PyTorch版本
    print(f"PyTorch版本: {torch.__version__}")
    
    # 检查MPS可用性
    mps_available = torch.backends.mps.is_available()
    print(f"MPS可用: {mps_available}")
    
    if mps_available:
        print("✅ MPS加速可用")
        
        # 测试设备
        device = torch.device("mps")
        print(f"使用设备: {device}")
        
        # 创建测试张量
        try:
            x = torch.randn(1000, 1000, device=device)
            y = torch.randn(1000, 1000, device=device)
            z = torch.mm(x, y)
            print("✅ MPS张量运算正常")
            
            # 测试YOLO模型加载
            try:
                print("正在下载YOLO模型...")
                model = YOLO('yolo8n.pt')  # 会自动下载模型
                print("✅ YOLO模型加载成功")
                
                # 测试模型推理
                import numpy as np
                test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
                results = model(test_image, device='mps', verbose=False)
                print("✅ YOLO MPS推理成功")
                
            except Exception as e:
                print(f"❌ YOLO MPS测试失败: {e}")
                print("提示: 首次运行会自动下载模型文件")
                
        except Exception as e:
            print(f"❌ MPS张量运算失败: {e}")
    else:
        print("❌ MPS不可用")
        print("可能原因:")
        print("1. 不是Apple Silicon芯片")
        print("2. PyTorch版本不支持MPS")
        print("3. macOS版本过低")

def test_device_selection():
    """测试设备选择逻辑"""
    print("\n=== 设备选择测试 ===")
    
    if torch.cuda.is_available():
        device = 'cuda'
        print("选择设备: CUDA")
    elif torch.backends.mps.is_available():
        device = 'mps'
        print("选择设备: MPS")
    else:
        device = 'cpu'
        print("选择设备: CPU")
    
    print(f"最终设备: {device}")
    return device

if __name__ == "__main__":
    test_mps()
    test_device_selection()
