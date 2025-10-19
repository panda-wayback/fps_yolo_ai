from typing import List, Tuple,Any

from ultralytics.engine.results import Boxes
from data_center.models.base_state import BaseState, ReactiveVar

class TargetSelectorModel(BaseState):
    """目标选择器状态类"""
    yolo_results: ReactiveVar[List[Any]] = None  # YOLO检测结果
    # 目标信息

    selected_target_bbox: ReactiveVar[Boxes] = None  # 选中目标的边界框 (x1, y1, x2, y2)
    selected_target_id: ReactiveVar[int] = 0  # 选中目标的ID

    # 准星比例
    crosshair_ratio: ReactiveVar[Tuple[float, float]] = (0.5, 0.45)  # 准星的X轴比例,Y轴比例

    # 准星位置
    crosshair_position: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)  # 准星位置 (x, y)

    # 选中目标的点比例 (x, y)
    target_point_ratio: ReactiveVar[Tuple[float, float]] = (0.5, 0.2)  # 选中目标的点比例 (x, y)

    # 距离目标的向量 (x, y)
    target_vector: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)  # 距离目标的向量 (x, y)

