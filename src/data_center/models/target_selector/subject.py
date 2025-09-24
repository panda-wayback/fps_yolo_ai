"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from typing import Any, List, Optional, Tuple
from data_center.models.target_selector.state import TargetSelectorState


class TargetSelectorSubject:
    """目标选择器订阅统一接口"""
    


    @staticmethod
    def send_yolo_results(yolo_results: List[Any] ):
        """发送YOLO检测结果进行目标选择"""
        TargetSelectorState.get_state().yolo_results.set(yolo_results)
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
        

