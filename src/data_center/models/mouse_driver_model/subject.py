"""
鼠标驱动模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Tuple
from data_center.models.mouse_driver_model.state_model import MouseDriverState
from data_center.models.mouse_driver_model.subject_model import MouseDriverSubjectModel
from data_center.models.mouse_driver_model.subjects.config import submit_config, update_mouse_driver_state
from data_center.models.mouse_driver_model.subjects.send_vector import submit_vector, update_data_center_vector


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



def init_config_subject():
    """初始化鼠标驱动配置订阅"""
    MouseDriverSubjectModel.config_subject.subscribe(submit_config)
    MouseDriverSubjectModel.config_subject.subscribe(update_mouse_driver_state)



def init_vector_subject():
    """初始化鼠标向量订阅"""
    MouseDriverSubjectModel.vector_subject.subscribe(submit_vector)
    MouseDriverSubjectModel.vector_subject.subscribe(update_data_center_vector)


def init_mouse_driver_subject_model():
    """初始化鼠标驱动所有话题绑定"""
    init_config_subject()
    init_vector_subject()


init_mouse_driver_subject_model()