
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器单例类
"""
import time
from typing import Optional, Tuple
from utils.controllers.adrc.ladrc import LADRCController
from utils.singleton.main import singleton

@singleton
class Controller:
    """PID控制器单例类"""
    
    def __init__(self):
        self.x_controller = LADRCController()
        self.y_controller = LADRCController()
        self.target_id = 0
        self.reset_time = time.time()
        
    
    def set_config(self, 
        order: Optional[int] = None, 
        sample_time: Optional[float] = None, 
        b0: Optional[float] = None, 
        w_cl: Optional[float] = None, 
        k_eso: Optional[float] = None,
        output_limits: Optional[Tuple[float, float]] = ...,  # 使用...作为哨兵值
        rate_limits: Optional[Tuple[float, float]] = ...):   # 使用...作为哨兵值
        """
        设置ADRC控制器参数 - 只修改传入的非None参数，未传入的参数保持原值
        
        Args:
            order: 控制器阶数 (1 或 2)，不传则保持原值
            sample_time: 采样时间（秒），不传则保持原值
            b0: 控制增益，不传则保持原值
            w_cl: 控制器带宽，不传则保持原值
            k_eso: ESO增益，不传则保持原值
            output_limits: 输出限幅 (min, max)，不传则保持原值
            rate_limits: 变化率限幅 (min, max)，不传则保持原值
        """
        # 使用关键字参数传递给子控制器（只传递非None的值）
        self.x_controller.set_config(
            order=order,
            sample_time=sample_time,
            b0=b0,
            w_cl=w_cl,
            k_eso=k_eso,
            output_limits=output_limits,
            rate_limits=rate_limits
        )
        self.y_controller.set_config(
            order=order,
            sample_time=sample_time,
            b0=b0,
            w_cl=w_cl,
            k_eso=k_eso,
            output_limits=output_limits,
            rate_limits=rate_limits
        )

    def compute(self, vector: tuple[float, float]) -> tuple[float, float]:
        """获取PID控制器输出"""
        try:
            x_output = self.x_controller.compute(vector[0])
            y_output = self.y_controller.compute(vector[1])
            return (x_output, y_output)
        except Exception as e:
            print(f"获取PID控制器输出失败: {e}")
            return (0.0, 0.0)
        
    def reset(self):
        """重置控制器"""
        self.x_controller.reset()
        self.y_controller.reset()
        
    def update_target_id(self, target_id: int):
        """更新目标ID"""
        
        if self.target_id == target_id and time.time() - self.reset_time < 0.35:
            return

        print(f"✅ 更新目标ID: {target_id}")
        self.reset_time = time.time()
        self.target_id = target_id
        self.reset()

# 全局单例实例
_controller = Controller()

def get_controller():
    """获取PID控制器单例"""
    return _controller

if __name__ == "__main__":
    pass