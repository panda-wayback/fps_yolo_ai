#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyDirectInput鼠标控制器测试
验证pydirectinput在Steam游戏中的兼容性
"""

import time
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.move_mouse.pydirectinput_controller import PyDirectInputMouseController
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


def test_pydirectinput_basic():
    """测试PyDirectInput基本功能"""
    print("🔧 测试PyDirectInput基本功能...")
    
    mouse = PyDirectInputMouseController()
    
    # 获取初始位置
    initial_pos = mouse.position
    print(f"📍 初始鼠标位置: {initial_pos}")
    
    # 测试相对移动
    print("🔄 测试相对移动...")
    mouse.move(100, 50)
    time.sleep(0.5)
    
    new_pos = mouse.position
    print(f"📍 移动后位置: {new_pos}")
    
    # 验证移动是否正确
    actual_dx = new_pos[0] - initial_pos[0]
    actual_dy = new_pos[1] - initial_pos[1]
    
    print(f"📏 期望移动: (100, 50)")
    print(f"📏 实际移动: ({actual_dx}, {actual_dy})")
    
    if abs(actual_dx - 100) <= 10 and abs(actual_dy - 50) <= 10:
        print("✅ 相对移动测试通过")
    else:
        print(f"❌ 相对移动测试失败 - 移动距离不准确")
        print(f"   可能的原因: DPI缩放、系统设置或权限问题")
    
    # 测试点击
    print("🖱️ 测试鼠标点击...")
    mouse.click('left')
    print("✅ 左键点击测试完成")
    
    return True


def test_pydirectinput_simulation():
    """测试PyDirectInput鼠标模拟器"""
    print("\n🎯 测试PyDirectInput鼠标模拟器...")
    
    simulator = get_mouse_simulator()
    
    # 启动模拟器
    simulator.run()
    print("✅ 鼠标模拟器已启动")
    
    # 提交测试向量
    print("📊 提交测试向量...")
    simulator.submit_vector((50, 30))  # 向右50像素，向下30像素
    
    # 等待一段时间让模拟器工作
    time.sleep(1)
    
    # 停止模拟器
    simulator.stop()
    print("✅ 鼠标模拟器已停止")
    
    return True


def test_steam_game_compatibility():
    """测试Steam游戏兼容性"""
    print("\n🎮 Steam游戏兼容性测试")
    print("=" * 50)
    print("请确保以下条件:")
    print("1. Steam正在运行")
    print("2. Aimlabs或其他Steam游戏已打开")
    print("3. 游戏窗口处于活动状态")
    print("4. 鼠标在游戏窗口内")
    print("=" * 50)
    
    input("按回车键开始测试...")
    
    mouse = PyDirectInputMouseController()
    
    print(f"📍 当前鼠标位置: {mouse.position}")
    
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
    print("- 如果鼠标在游戏中正常移动，说明PyDirectInput方法有效")
    print("- PyDirectInput专门为游戏设计，兼容性更好")
    print("- 移动距离应该更准确，不受DPI缩放影响")


def test_precision_movement():
    """测试精确移动"""
    print("\n🎯 精确移动测试")
    print("=" * 30)
    
    mouse = PyDirectInputMouseController()
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


def main():
    """主测试函数"""
    print("🚀 开始测试PyDirectInput鼠标控制器...")
    print("=" * 60)
    
    try:
        # 基本功能测试
        test_pydirectinput_basic()
        
        # 模拟器测试
        test_pydirectinput_simulation()
        
        # Steam游戏兼容性测试
        test_steam_game_compatibility()
        
        # 精确移动测试
        test_precision_movement()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("\n💡 使用说明:")
        print("- PyDirectInput鼠标控制器已替换pynput")
        print("- 专门为游戏设计，Steam兼容性更好")
        print("- 支持精确的像素级移动控制")
        print("- 不受DPI缩放影响")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
