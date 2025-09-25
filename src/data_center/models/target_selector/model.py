from typing import List, Tuple,Any
from data_center.models.base_state import BaseState, ReactiveVar


class TargetSelectorModel(BaseState):
    """目标选择器状态类"""
    yolo_results: ReactiveVar[List[Any]] = None  # YOLO检测结果
    # 目标信息
    selected_target_point: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)  # 选中目标的中心点 (x, y)
    selected_target_bbox: ReactiveVar[Tuple[float, float, float, float]] = None  # 选中目标的边界框 (x1, y1, x2, y2)
    selected_target_confidence: ReactiveVar[float] = None  # 选中目标的置信度
    selected_target_class_id: ReactiveVar[int] = None  # 选中目标的类别ID
    