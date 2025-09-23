
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器单例类
"""
from threading import Lock
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
    
    def set_pid_parameters(self, 
        kp: float,
        ki: float,
        kd: float
    ):
        """设置PID参数"""
        self.pid_control.set_pid_parameters(kp, ki, kd)

    def get_vector_pid_res(self, vector: tuple[float, float], dt=0.02) -> tuple[tuple[float, float], tuple[float, float]]:
        """获取PID控制器输出"""
        if vector is None:
            return (0.0, 0.0), (0.0, 0.0)
        error_x, error_y = vector
        x_output, y_output = self.pid_control.update(error_x, error_y, dt)
        print(f"PID控制器输出: x_output={x_output}, y_output={y_output}")   
        return (x_output, y_output), (error_x, error_y)

# 全局单例实例
_pid_controller = PIDController()

def get_pid_controller():
    """获取PID控制器单例"""
    return _pid_controller


if __name__ == "__main__":
    from data_center.models.pid_model.subject import PIDSubject
    PIDSubject.send_config(1.0, 0.0, 0.0)