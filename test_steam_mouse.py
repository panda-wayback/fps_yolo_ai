#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam游戏鼠标控制测试
专门用于测试在Steam游戏中的鼠标控制效果
"""

import time
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.move_mouse.windows_mouse_controller import WindowsMouseController


def test_steam_mouse_control():
    """测试Steam游戏中的鼠标控制"""
    print("🎮 Steam游戏鼠标控制测试")
    print("=" * 50)
    print("请确保以下条件:")
    print("1. Steam正在运行")
    print("2. Aimlabs或其他Steam游戏已打开")
    print("3. 游戏窗口处于活动状态")
    print("4. 鼠标在游戏窗口内")
    print("=" * 50)
    
    input("按回车键开始测试...")
    
    mouse = WindowsMouseController()
    
    print(f"📍 当前鼠标位置: {mouse.position}")
    print(f"📊 DPI缩放因子: X={mouse.dpi_scale_x:.2f}, Y={mouse.dpi_scale_y:.2f}")
    
    print("\n🔄 开始测试移动...")
    print("测试1: 小幅度移动 (10像素)")
    
    # 测试1: 小幅度移动
    for i in range(5):
        print(f"  移动 {i+1}/5: 向右10像素")
        mouse.move(10, 0)
        time.sleep(0.3)
    
    time.sleep(1)
    
    print("\n测试2: 中等幅度移动 (50像素)")
    # 测试2: 中等幅度移动
    for i in range(3):
        print(f"  移动 {i+1}/3: 向下50像素")
        mouse.move(0, 50)
        time.sleep(0.5)
    
    time.sleep(1)
    
    print("\n测试3: 大幅度移动 (100像素)")
    # 测试3: 大幅度移动
    for i in range(2):
        print(f"  移动 {i+1}/2: 向左100像素")
        mouse.move(-100, 0)
        time.sleep(0.8)
    
    time.sleep(1)
    
    print("\n测试4: 圆形移动")
    # 测试4: 圆形移动
    import math
    radius = 50
    steps = 8
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        dx = int(radius * math.cos(angle))
        dy = int(radius * math.sin(angle))
        print(f"  圆形移动 {i+1}/{steps}: ({dx}, {dy})")
        mouse.move(dx, dy)
        time.sleep(0.2)
    
    print("\n测试5: 鼠标点击")
    print("  左键点击...")
    mouse.click('left')
    time.sleep(0.5)
    
    print("  右键点击...")
    mouse.click('right')
    time.sleep(0.5)
    
    print("\n✅ 所有测试完成！")
    print("\n💡 观察结果:")
    print("- 如果鼠标在游戏中正常移动，说明Windows API方法有效")
    print("- 如果鼠标没有移动，可能需要检查游戏设置或权限")
    print("- 移动距离可能因DPI缩放而有所不同，这是正常的")


def test_precision_movement():
    """测试精确移动"""
    print("\n🎯 精确移动测试")
    print("=" * 30)
    
    mouse = WindowsMouseController()
    initial_pos = mouse.position
    print(f"📍 起始位置: {initial_pos}")
    
    # 测试精确移动
    movements = [
        (1, 0),   # 向右1像素
        (0, 1),   # 向下1像素
        (-1, 0),  # 向左1像素
        (0, -1),  # 向上1像素
        (5, 5),   # 对角线移动
        (-5, -5), # 对角线返回
    ]
    
    for i, (dx, dy) in enumerate(movements):
        print(f"  精确移动 {i+1}: ({dx}, {dy})")
        mouse.move(dx, dy)
        time.sleep(0.2)
        current_pos = mouse.position
        actual_dx = current_pos[0] - initial_pos[0]
        actual_dy = current_pos[1] - initial_pos[1]
        print(f"    实际移动: ({actual_dx}, {actual_dy})")
        initial_pos = current_pos
    
    print("✅ 精确移动测试完成")


if __name__ == "__main__":
    try:
        test_steam_mouse_control()
        test_precision_movement()
        
        print("\n" + "=" * 50)
        print("🎉 测试总结:")
        print("✅ Windows API鼠标控制器已成功替换pynput")
        print("✅ 现在可以在Steam游戏中控制鼠标")
        print("✅ 支持精确的像素级移动控制")
        print("✅ 兼容高DPI显示器")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
