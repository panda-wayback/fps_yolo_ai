
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器单例类
"""

from threading import Lock
from functions.get_target_vector import get_center_to_target_vector
from utils.pid.pid import PIDControl


class PIDController:
    """PID控制器单例类"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.pid_control = PIDControl()
        self._initialized = True
    
    def get_pid_parameters(self):
        """获取PID参数"""
        return self.pid_control.get_pid_parameters()
    
    def set_pid_parameters(self, kp, ki, kd):
        """设置PID参数"""
        self.pid_control.set_pid_parameters(kp, ki, kd)
    
    def get_pid_res(self, results, image_size, dt=0.02) -> tuple[float, float]:
        """
        获取PID控制器输出
        
        Args:
            results: YOLO检测结果
            image_size: 图像尺寸 (width, height)
            dt: 时间步长
        
        Returns:
            tuple: (x_output, y_output) 或 (0, 0) 如果没有目标
        """
        # 获取目标向量
        vector_result = get_center_to_target_vector(results, image_size)
        
        if vector_result is None:
            return (0, 0)
        
        error_x, error_y = vector_result
        
        # 使用PID控制器计算输出
        x_output, y_output = self.pid_control.update(error_x, error_y, dt)
        
        return x_output, y_output


# 全局单例实例
_pid_controller = PIDController()

# 便捷函数
def get_pid_parameters():
    """获取PID参数"""
    return _pid_controller.get_pid_parameters()

def set_pid_parameters(kp, ki, kd):
    """设置PID参数"""
    _pid_controller.set_pid_parameters(kp, ki, kd)

def get_pid_res(results, image_size, dt=0.02) -> tuple[float, float]:
    """获取PID控制器输出"""
    return _pid_controller.get_pid_res(results, image_size, dt)