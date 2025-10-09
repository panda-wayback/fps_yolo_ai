#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制策略
使用 simple_pid 库实现双轴 PID 控制器
适用于 FPS 游戏中的瞄准控制，可以同时控制 X 和 Y 轴的运动

特性：
- 支持KI条件控制：距离目标10像素内使用KI，其余时候KI为0
- 避免积分饱和，提高控制性能
- 可动态调整KI激活距离阈值
"""

from simple_pid import PID


class PIDControl:
    """
    双轴 PID 控制器类
    
    该类实现了两个独立的 PID 控制器，分别用于控制 X 轴和 Y 轴的运动。
    适用于需要精确位置控制的场景，如 FPS 游戏中的瞄准辅助。
    
    特性：
    - 支持独立的 X/Y 轴控制
    - 可调节的 PID 参数
    - 输出限制保护
    - 手动时间步长控制
    """
    
    def __init__(self, kp=10, ki=0, kd=0.05, v_limit=200000.0, ki_distance_threshold=20.0):
        """
        初始化双轴 PID 控制器
        
        Args:
            kp (float): 比例增益，控制响应速度
                       值越大，系统对误差的响应越快，但可能导致超调
                       默认值: 10.0
            ki (float): 积分增益，消除稳态误差
                       值越大，消除稳态误差的能力越强，但可能导致振荡
                       默认值: 0.01
            kd (float): 微分增益，提供阻尼和预测性
                       值越大，系统越稳定，但可能对噪声敏感
                       默认值: 0.2
            v_limit (float): 输出速度限制，防止输出过大
                            单位：像素/秒或相应的速度单位
                            默认值: 200000.0
            ki_distance_threshold (float): KI激活的距离阈值
                                          距离目标在此范围内时使用KI，否则KI为0
                                          默认值: 10.0
        """
        # 保存KI距离阈值
        self.ki_distance_threshold = ki_distance_threshold
        # 创建 X 轴 PID 控制器
        # 目标值设为 0，表示我们希望误差为 0（即到达目标位置）
        self.pid_x = PID(
            Kp=kp,           # 比例增益
            Ki=ki,           # 积分增益  
            Kd=kd,           # 微分增益
            setpoint=0.0,    # 目标值设为 0（误差为 0）
            output_limits=(-v_limit, v_limit),  # 输出限制，防止速度过大
            sample_time=None  # 禁用自动时间控制，我们手动传入 dt
        )
        
        # 创建 Y 轴 PID 控制器，参数与 X 轴相同
        self.pid_y = PID(
            Kp=kp,           # 比例增益
            Ki=ki,           # 积分增益
            Kd=kd,           # 微分增益
            setpoint=0.0,    # 目标值设为 0（误差为 0）
            output_limits=(-v_limit, v_limit),  # 输出限制，防止速度过大
            sample_time=None  # 禁用自动时间控制，我们手动传入 dt
        )
        
    
    def update(self, error_x: float, error_y: float, dt: float) -> tuple[float, float]:
        """
        更新 PID 控制器并计算输出
        
        该方法接收当前 X 和 Y 轴的误差，以及时间步长，
        然后计算相应的控制输出。
        
        Args:
            error_x (float): X 轴误差值
                            正值表示目标在当前位置右侧，负值表示在左侧
                            单位：像素或相应的距离单位
            error_y (float): Y 轴误差值  
                            正值表示目标在当前位置下方，负值表示在上方
                            单位：像素或相应的距离单位
            dt (float): 时间步长，两次调用之间的时间间隔
                       单位：秒
                       用于计算微分项和积分项
                       
        Returns:
            tuple[float, float]: (x_output, y_output) 控制输出
                x_output: X 轴的控制输出，正值表示向右移动，负值表示向左移动
                y_output: Y 轴的控制输出，正值表示向下移动，负值表示向上移动
                单位：像素/秒或相应的速度单位
                
        注意：
        - 输出值已被限制在 [-v_limit, v_limit] 范围内
        - 如果误差为 0，输出也应该接近 0
        - 时间步长 dt 应该尽可能准确，以获得最佳控制效果
        """
        # 确保目标值始终为 0（我们希望误差为 0）
        self.pid_x.setpoint = 0
        self.pid_y.setpoint = 0

        # 更新 X 轴 PID 控制器
        # 传入当前误差值和时间步长，计算控制输出
        x_output = self.pid_x(error_x, dt=dt)
        
        # 更新 Y 轴 PID 控制器  
        # 传入当前误差值和时间步长，计算控制输出
        y_output = self.pid_y(error_y, dt=dt)

        # 返回两个轴的控制输出
        # x_output: X 轴移动速度，正值向右，负值向左
        # y_output: Y 轴移动速度，正值向下，负值向上
        return x_output, y_output
    
    def set_ki_distance_threshold(self, threshold):
        """
        设置KI激活的距离阈值
        
        Args:
            threshold (float): 新的距离阈值，单位：像素
        """
        self.ki_distance_threshold = threshold
        print(f"✅ KI距离阈值更新为: {threshold} 像素")
    
    def get_ki_distance_threshold(self):
        """
        获取当前KI距离阈值
        
        Returns:
            float: 当前的距离阈值
        """
        return self.ki_distance_threshold
    
    # 修改pid参数
    def set_pid_parameters(self, kp, ki, kd):
        """
        设置PID参数
        """
        self.pid_x.Kp = kp
        self.pid_x.Ki = ki
        self.pid_x.Kd = kd
    
    # 获取pid参数
    def get_pid_parameters(self):
        """
        获取PID参数
        """
        return self.pid_x.Kp, self.pid_x.Ki, self.pid_x.Kd

