"""
鼠标驱动模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Tuple
from data_center.models.mouse_driver_model.state_model import MouseDriverState
from data_center.models.mouse_driver_model.subject_model import MouseDriverSubjectModel


class MouseDriverSubject:
    """鼠标驱动模型订阅统一接口"""
    
    @staticmethod
    def send_config(config: MouseDriverState):
        """发送鼠标驱动配置"""
        MouseDriverSubjectModel.config_subject.on_next(config)
    
    @staticmethod
    def send_vector(vector: Tuple[float, float]):
        """发送鼠标向量"""
        MouseDriverSubjectModel.vector_subject.on_next(vector)
    
    @staticmethod
    def get_state():
        """获取鼠标驱动状态"""
        from data_center.index import get_data_center
        return get_data_center().state.mouse_driver_state