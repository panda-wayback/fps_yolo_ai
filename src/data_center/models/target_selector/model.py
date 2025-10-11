from typing import List, Tuple,Any

from ultralytics.engine.results import Boxes
from data_center.models.base_state import BaseState, ReactiveVar


class TargetSelectorModel(BaseState):
    """目标选择器状态类"""
    yolo_results: ReactiveVar[List[Any]] = None  # YOLO检测结果
    # 目标信息
    selected_target_point: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)  # 选中目标的中心点 (x, y)
    selected_target_bbox: ReactiveVar[Boxes] = None  # 选中目标的边界框 (x1, y1, x2, y2)
    selected_target_id: ReactiveVar[int] = 0  # 选中目标的ID