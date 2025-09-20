"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from typing import Optional, Tuple
from data_center.models.target_selector.state_model import TargetSelectorState
from data_center.models.target_selector.subject_model import TargetSelectorSubjectModel
from data_center.models.target_selector.subjects.config import set_target_selector_config
from data_center.models.target_selector.subjects.select_target import set_target_select_subject


class TargetSelectorSubject:
    """目标选择器订阅统一接口"""
    
    @staticmethod
    def send_yolo_results(yolo_results):
        """发送YOLO检测结果进行目标选择"""
        TargetSelectorSubjectModel.select_subject.on_next(yolo_results)
    
    @staticmethod
    def set_config(
        distance_weight: Optional[float] = None,
        confidence_weight: Optional[float] = None,
        similarity_weight: Optional[float] = None,
        class_weight: Optional[float] = None,
        reference_vector: Optional[Tuple[float, float]] = None
    ):
        """设置目标选择器配置"""
        config_data = {}
        if distance_weight is not None:
            config_data['distance_weight'] = distance_weight
        if confidence_weight is not None:
            config_data['confidence_weight'] = confidence_weight
        if similarity_weight is not None:
            config_data['similarity_weight'] = similarity_weight
        if class_weight is not None:
            config_data['class_weight'] = class_weight
        if reference_vector is not None:
            config_data['reference_vector'] = reference_vector
        
        config = TargetSelectorState(**config_data)
        TargetSelectorSubjectModel.config_subject.on_next(config)
    
    @staticmethod
    def get_state():
        """获取目标选择器状态"""
        from data_center.index import get_data_center
        return get_data_center().state.target_selector_state

def init_config_subject():
    """初始化目标选择器配置订阅"""
    TargetSelectorSubjectModel.config_subject.subscribe(set_target_selector_config)

def init_select_subject():
    """初始化目标选择订阅"""
    TargetSelectorSubjectModel.select_subject.subscribe(set_target_select_subject)

def init_target_selector_subject_model():
    """初始化目标选择器所有话题绑定"""
    init_config_subject()
    init_select_subject()


init_target_selector_subject_model()