
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器单例类
"""
from typing import Optional, Tuple
from utils.controllers.adrc.ladrc import LADRCController
from utils.singleton.main import singleton


@singleton
class Controller:
    """PID控制器单例类"""
    
    def __init__(self):
        self.x_controller = LADRCController()
        self.y_controller = LADRCController()
    
    def set_config(self, 
        order: int = 1, 
        sample_time: float = 0.01, 
        b0: float = 1.0, 
        w_cl: float = 60.0, 
        k_eso: float = 2.5,
        output_limits: Optional[Tuple[float, float]] = None,
        rate_limits: Optional[Tuple[float, float]] = None):
        
        """设置ADRC控制器参数"""
        self.x_controller.set_config(order, sample_time, b0, w_cl, k_eso, output_limits, rate_limits)
        self.y_controller.set_config(order, sample_time, b0, w_cl, k_eso, output_limits, rate_limits)

    def get_vector_pid_res(self, vector: tuple[float, float], dt=0.02) -> tuple[tuple[float, float], tuple[float, float]]:
        """获取PID控制器输出"""
        try:
            error_x, error_y = vector
            x_output, y_output = self.pid_control.update(error_x, error_y, dt)
            return (x_output, y_output), (error_x, error_y)
        except Exception as e:
            print(f"获取PID控制器输出失败: {e}")
            return (0.0, 0.0), (0.0, 0.0)

# 全局单例实例
_controller = Controller()

def get_controller():
    """获取PID控制器单例"""
    return _controller

if __name__ == "__main__":
    pass