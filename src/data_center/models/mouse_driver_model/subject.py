"""
鼠标驱动模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Optional, Tuple
from data_center.models.mouse_driver_model.state import MouseDriverState
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator

class MouseDriverSubject:
    """鼠标驱动模型订阅统一接口"""
    
    @staticmethod
    def send_config(
        smoothing: Optional[float] = None,
        fps: Optional[int] = None,
        running: Optional[bool] = None,
        max_duration: Optional[float] = None,
        decay_rate: Optional[float] = None,
    ):
        """发送鼠标驱动配置"""
        if smoothing is not None:
            MouseDriverState.get_state().smoothing.set(smoothing)
        if fps is not None:
            MouseDriverState.get_state().fps.set(fps)
            MouseDriverState.get_state().interval.set(1.0 / fps)
        if running is not None:
            MouseDriverState.get_state().running.set(running)
        if max_duration is not None:
            MouseDriverState.get_state().max_duration.set(max_duration)
        if decay_rate is not None:
            MouseDriverState.get_state().decay_rate.set(decay_rate)
        
        get_mouse_simulator().run()
    
    @staticmethod
    def send_vector(vector: Tuple[float, float]):
        """发送鼠标向量"""
        MouseDriverState.get_state().vector.set(vector)

    
    
