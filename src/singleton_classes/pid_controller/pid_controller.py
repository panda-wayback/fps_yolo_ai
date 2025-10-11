
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器单例类
"""
from utils.controllers.pid.pid import PIDControl
from utils.singleton.main import singleton


@singleton
class PIDController:
    """PID控制器单例类"""
    
    def __init__(self):
        self.pid_control = PIDControl()
    
    def set_pid_parameters(self, 
        kp: float,
        ki: float,
        kd: float
    ):
        """设置PID参数"""
        self.pid_control.set_pid_parameters(kp, ki, kd)

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
_pid_controller = PIDController()

def get_pid_controller():
    """获取PID控制器单例"""
    return _pid_controller


if __name__ == "__main__":
    from data_center.models.pid_model.subject import PIDSubject
    PIDSubject.send_config(1.0, 0.0, 0.0)