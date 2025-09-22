"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from typing import Any, List, Optional, Tuple
from data_center.models.target_selector.state import TargetSelectorState
from singleton_classes.target_selector.target_selector import get_target_selector


class TargetSelectorSubject:
    """目标选择器订阅统一接口"""
    


    @staticmethod
    def send_yolo_results(yolo_results: List[Any]):
        """发送YOLO检测结果进行目标选择"""
        selected_point, selected_bbox, selected_confidence, selected_class_id  = get_target_selector().target_selector(yolo_results)
        TargetSelectorState.get_state().selected_target_point.set(selected_point)
        TargetSelectorState.get_state().selected_target_bbox.set(selected_bbox)
        TargetSelectorState.get_state().selected_target_confidence.set(selected_confidence)
        TargetSelectorState.get_state().selected_target_class_id.set(selected_class_id)
        pass
    
    @staticmethod
    def set_config(
        distance_weight: Optional[float] = None,
        confidence_weight: Optional[float] = None,
        similarity_weight: Optional[float] = None,
        class_weight: Optional[float] = None,
        reference_vector: Optional[Tuple[float, float]] = None
    ):
        if distance_weight is not None:
            TargetSelectorState.get_state().distance_weight.set(distance_weight)
        if confidence_weight is not None:
            TargetSelectorState.get_state().confidence_weight.set(confidence_weight)
        if similarity_weight is not None:
            TargetSelectorState.get_state().similarity_weight.set(similarity_weight)
        if class_weight is not None:
            TargetSelectorState.get_state().class_weight.set(class_weight)
        if reference_vector is not None:
            TargetSelectorState.get_state().reference_vector.set(reference_vector)
        

