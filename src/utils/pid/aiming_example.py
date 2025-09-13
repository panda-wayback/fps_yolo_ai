#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瞄准控制示例
展示如何使用 PID 控制器进行瞄准控制
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pid.pid import PIDControl


def aiming_control_example():
    """
    瞄准控制示例
    
    模拟 FPS 游戏中的瞄准控制场景：
    1. 检测到目标
    2. 计算目标与准星的向量
    3. 使用 PID 控制器计算鼠标移动量
    4. 模拟鼠标移动
    """
    print("=== 瞄准控制示例 ===")
    
    # 创建 PID 控制器
    # 参数说明：
    # kp=1.5: 比例增益，控制响应速度
    # ki=0.1: 积分增益，消除稳态误差
    # kd=0.3: 微分增益，提供阻尼
    # v_limit=100.0: 最大移动速度限制
    pid_controller = PIDControl(kp=1.5, ki=0.1, kd=0.3, v_limit=100.0)
    
    # 模拟参数
    image_center_x = 200.0  # 图像中心 X 坐标（准星位置）
    image_center_y = 150.0  # 图像中心 Y 坐标（准星位置）
    
    # 模拟检测到的目标位置
    target_positions = [
        (250, 180),  # 目标1：右下
        (150, 120),  # 目标2：左上
        (200, 150),  # 目标3：正中（测试收敛）
        (300, 100),  # 目标4：右上
    ]
    
    for i, (target_x, target_y) in enumerate(target_positions):
        print(f"\n--- 目标 {i+1}: 位置 ({target_x}, {target_y}) ---")
        
        # 计算目标与准星的向量
        error_x = target_x - image_center_x
        error_y = target_y - image_center_y
        distance = (error_x**2 + error_y**2)**0.5
        
        print(f"初始误差: X={error_x:.1f}, Y={error_y:.1f}, 距离={distance:.1f}")
        
        # 模拟瞄准过程
        current_x, current_y = image_center_x, image_center_y
        dt = 0.016  # 约 60 FPS
        
        for step in range(50):  # 最多 50 步
            # 计算当前误差
            current_error_x = target_x - current_x
            current_error_y = target_y - current_y
            current_distance = (current_error_x**2 + current_error_y**2)**0.5
            
            # 使用 PID 控制器计算移动量
            move_x, move_y = pid_controller.update_dual(current_error_x, current_error_y, dt)
            
            # 模拟鼠标移动（更新当前位置）
            current_x += move_x * dt
            current_y += move_y * dt
            
            # 打印状态（每 10 步打印一次）
            if step % 10 == 0:
                print(f"步骤 {step:2d}: 位置=({current_x:.1f}, {current_y:.1f}), "
                      f"误差=({current_error_x:.1f}, {current_error_y:.1f}), "
                      f"移动=({move_x:.1f}, {move_y:.1f}), 距离={current_distance:.1f}")
            
            # 检查是否收敛
            if current_distance < 2.0:  # 误差小于 2 像素认为已收敛
                print(f"✓ 瞄准完成！用时 {step+1} 步，最终距离: {current_distance:.1f}")
                break
        
        # 重置 PID 控制器状态
        pid_controller.reset()
        
        # 等待一下
        time.sleep(0.5)


def real_time_aiming_simulation():
    """
    实时瞄准模拟
    
    模拟实时瞄准控制，展示如何在实际游戏中使用
    """
    print("\n=== 实时瞄准模拟 ===")
    
    # 创建 PID 控制器
    pid_controller = PIDControl(kp=2.0, ki=0.05, kd=0.4, v_limit=80.0)
    
    # 模拟参数
    image_center_x = 200.0
    image_center_y = 150.0
    
    # 模拟目标移动轨迹
    target_trajectory = [
        (220, 160), (240, 170), (260, 180), (280, 190),  # 向右下移动
        (270, 180), (250, 170), (230, 160), (210, 150),  # 向左上移动
        (200, 150),  # 回到中心
    ]
    
    current_x, current_y = image_center_x, image_center_y
    dt = 0.016  # 60 FPS
    
    print("开始实时瞄准模拟...")
    print("目标轨迹: 右下 -> 左上 -> 中心")
    
    for i, (target_x, target_y) in enumerate(target_trajectory):
        # 计算误差
        error_x = target_x - current_x
        error_y = target_y - current_y
        distance = (error_x**2 + error_y**2)**0.5
        
        # 使用 PID 控制器计算移动量
        move_x, move_y = pid_controller.update_dual(error_x, error_y, dt)
        
        # 更新当前位置
        current_x += move_x * dt
        current_y += move_y * dt
        
        # 打印状态
        print(f"帧 {i+1:2d}: 目标=({target_x:3.0f}, {target_y:3.0f}), "
              f"准星=({current_x:5.1f}, {current_y:5.1f}), "
              f"误差=({error_x:5.1f}, {error_y:5.1f}), "
              f"移动=({move_x:5.1f}, {move_y:5.1f}), 距离={distance:5.1f}")
        
        # 模拟帧间隔
        time.sleep(0.1)  # 实际游戏中不需要这个延迟
    
    print("实时瞄准模拟完成！")


if __name__ == "__main__":
    """
    主函数：运行瞄准控制示例
    """
    print("PID 瞄准控制系统示例")
    print("=" * 50)
    
    try:
        # 运行基本瞄准控制示例
        aiming_control_example()
        
        # 运行实时瞄准模拟
        real_time_aiming_simulation()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        
    except Exception as e:
        print(f"运行示例时发生错误: {e}")
        print("请确保 simple_pid 库已正确安装")
        print("安装命令: pip install simple-pid")
