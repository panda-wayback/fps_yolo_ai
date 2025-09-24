#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MPS测试脚本
验证macOS的MPS加速是否正常工作
"""

import torch
import time
import numpy as np
from ultralytics import YOLO


def test_mps_availability():
    """测试MPS可用性"""
    print("=== MPS可用性测试 ===")
    
    # 检查MPS是否可用
    mps_available = torch.backends.mps.is_available()
    print(f"MPS可用: {'✅ 是' if mps_available else '❌ 否'}")
    
    if not mps_available:
        print("❌ MPS不可用，可能的原因:")
        print("  1. macOS版本过低（需要macOS 12.3+）")
        print("  2. PyTorch版本过低（需要1.12+）")
        print("  3. 没有Apple Silicon芯片")
        return False
    
    # 检查MPS是否已构建
    mps_built = torch.backends.mps.is_built()
    print(f"MPS已构建: {'✅ 是' if mps_built else '❌ 否'}")
    
    return True


def test_mps_performance():
    """测试MPS性能"""
    print("\n=== MPS性能测试 ===")
    
    if not torch.backends.mps.is_available():
        print("❌ MPS不可用，跳过性能测试")
        return
    
    # 创建测试张量
    size = (1000, 1000)
    
    # CPU测试
    print("CPU性能测试...")
    cpu_tensor = torch.randn(size)
    
    start_time = time.time()
    for _ in range(100):
        result = torch.matmul(cpu_tensor, cpu_tensor)
    cpu_time = time.time() - start_time
    print(f"CPU时间: {cpu_time:.3f}秒")
    
    # MPS测试
    print("MPS性能测试...")
    mps_tensor = torch.randn(size, device='mps')
    
    start_time = time.time()
    for _ in range(100):
        result = torch.matmul(mps_tensor, mps_tensor)
    mps_time = time.time() - start_time
    print(f"MPS时间: {mps_time:.3f}秒")
    
    # 性能比较
    speedup = cpu_time / mps_time
    print(f"加速比: {speedup:.2f}x")
    
    if speedup > 1:
        print("✅ MPS加速有效")
    else:
        print("⚠️  MPS加速效果不明显")


def test_yolo_with_mps():
    """测试YOLO模型在MPS上的运行"""
    print("\n=== YOLO MPS测试 ===")
    
    if not torch.backends.mps.is_available():
        print("❌ MPS不可用，跳过YOLO测试")
        return
    
    try:
        # 加载预训练模型
        print("加载YOLO模型...")
        model = YOLO('yolov8n.pt')  # 使用较小的模型进行测试
        
        # 移动到MPS设备
        model.to('mps')
        print("模型已移动到MPS设备")
        
        # 创建测试图像
        test_img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        # 预热
        print("预热模型...")
        for _ in range(3):
            _ = model(test_img, verbose=False)
        
        # 测试推理时间
        print("测试推理性能...")
        start_time = time.time()
        for _ in range(10):
            results = model(test_img, verbose=False)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        print(f"平均推理时间: {avg_time*1000:.1f} ms")
        print(f"推理FPS: {1/avg_time:.1f}")
        
        print("✅ YOLO MPS测试成功")
        
    except Exception as e:
        print(f"❌ YOLO MPS测试失败: {e}")
        print("可能的原因:")
        print("  1. 模型不支持MPS")
        print("  2. 内存不足")
        print("  3. MPS驱动问题")


def test_memory_usage():
    """测试内存使用情况"""
    print("\n=== 内存使用测试 ===")
    
    if not torch.backends.mps.is_available():
        print("❌ MPS不可用，跳过内存测试")
        return
    
    try:
        # 检查初始内存
        initial_memory = torch.mps.current_allocated_memory()
        print(f"初始MPS内存: {initial_memory / 1024**2:.1f} MB")
        
        # 分配一些内存
        tensors = []
        for i in range(5):
            tensor = torch.randn(1000, 1000, device='mps')
            tensors.append(tensor)
            current_memory = torch.mps.current_allocated_memory()
            print(f"分配张量 {i+1}: {current_memory / 1024**2:.1f} MB")
        
        # 释放内存
        del tensors
        torch.mps.empty_cache()
        
        final_memory = torch.mps.current_allocated_memory()
        print(f"释放后MPS内存: {final_memory / 1024**2:.1f} MB")
        
        print("✅ 内存管理正常")
        
    except Exception as e:
        print(f"❌ 内存测试失败: {e}")


if __name__ == "__main__":
    print("🧪 MPS测试脚本")
    print("=" * 40)
    
    # 运行所有测试
    if test_mps_availability():
        test_mps_performance()
        test_yolo_with_mps()
        test_memory_usage()
    
    print("\n测试完成！")

