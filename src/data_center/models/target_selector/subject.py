"""
目标选择器相关的统一接口
"""

from data_center.index import get_data_center
from data_center.models.target_selector.subjects.select_target import use_target_select_subject
from data_center.models.target_selector.subjects.config import use_target_selector_config_subject
from typing import Optional, Tuple


class TargetSelectorSubject:
    """目标选择器订阅统一接口"""
    
    @staticmethod
    def send_yolo_results(yolo_results):
        """发送YOLO检测结果进行目标选择"""
        use_target_select_subject(yolo_results)
    
    @staticmethod
    def set_config(
        distance_weight: Optional[float] = None,
        confidence_weight: Optional[float] = None,
        similarity_weight: Optional[float] = None,
        class_weight: Optional[float] = None,
        reference_vector: Optional[Tuple[float, float]] = None
    ):
        """设置目标选择器配置"""
        use_target_selector_config_subject(
            distance_weight=distance_weight,
            confidence_weight=confidence_weight,
            similarity_weight=similarity_weight,
            class_weight=class_weight,
            reference_vector=reference_vector
        )
    
    @staticmethod
    def get_state():
        """获取目标选择器状态"""
        return get_data_center().state.target_selector_state
