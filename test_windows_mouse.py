#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Windows鼠标控制器
验证新的鼠标控制器是否能正常工作，特别是与Steam游戏的兼容性
"""

import time
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.move_mouse.windows_mouse_controller import WindowsMouseController
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


def test_basic_mouse_control():
    """测试基本鼠标控制功能"""
    print("🔧 测试基本鼠标控制功能...")
    time.sleep(5)
    mouse = WindowsMouseController()
    
    # 显示DPI信息
    print(f"📊 DPI缩放因子: X={mouse.dpi_scale_x:.2f}, Y={mouse.dpi_scale_y:.2f}")
    print(f"📺 屏幕尺寸: {mouse.screen_width}x{mouse.screen_height}")
    
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
    expected_x = initial_pos[0] + 100
    expected_y = initial_pos[1] + 50
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


def test_simulation_mouse():
    """测试鼠标模拟器"""
    print("\n🎯 测试鼠标模拟器...")
    
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


def test_steam_compatibility():
    """测试Steam游戏兼容性提示"""
    print("\n🎮 Steam游戏兼容性测试提示:")
    print("1. 请确保Steam和Aimlabs正在运行")
    print("2. 将鼠标移动到Aimlabs游戏窗口内")
    print("3. 运行以下命令进行测试:")
    print("   python test_windows_mouse.py --steam-test")
    print("4. 观察鼠标是否能在游戏内正常移动")
    
    return True


def main():
    """主测试函数"""
    print("🚀 开始测试Windows鼠标控制器...")
    print("=" * 50)
    
    try:
        # 基本功能测试
        test_basic_mouse_control()
        
        # 模拟器测试
        test_simulation_mouse()
        
        # Steam兼容性提示
        test_steam_compatibility()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成！")
        print("\n💡 使用说明:")
        print("- 新的Windows API鼠标控制器已替换pynput")
        print("- 现在应该可以在Steam游戏中正常控制鼠标")
        print("- 如果仍有问题，请检查游戏的反作弊设置")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--steam-test":
        print("🎮 开始Steam游戏兼容性测试...")
        print("请确保Aimlabs正在运行，并将鼠标移动到游戏窗口内")
        input("按回车键开始测试...")
        
        # 在Steam游戏中测试
        mouse = WindowsMouseController()
        print("📍 当前鼠标位置:", mouse.position)
        
        print("🔄 执行测试移动...")
        for i in range(5):
            mouse.move(20, 0)  # 向右移动
            time.sleep(0.2)
        
        for i in range(5):
            mouse.move(0, 20)  # 向下移动
            time.sleep(0.2)
        
        for i in range(5):
            mouse.move(-20, 0)  # 向左移动
            time.sleep(0.2)
        
        for i in range(5):
            mouse.move(0, -20)  # 向上移动
            time.sleep(0.2)
        
        print("✅ Steam兼容性测试完成！")
        print("如果鼠标在Aimlabs中正常移动，说明兼容性测试通过！")
    else:
        main()
