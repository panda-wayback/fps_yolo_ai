from typing import List, Any

from ultralytics.engine.results import Boxes

from data_center.models.target_selector.state import TargetSelectorState
from singleton_classes.target_selector.target_selector import get_target_selector

# 选择目标边框
def select_target(yolo_results: List[Any]):
    if not yolo_results:
        return
    crosshair_ratio = TargetSelectorState.get_state().crosshair_ratio.get()

    # 计算准星位置
    h, w = yolo_results[0].orig_shape
    crosshair_ratio = TargetSelectorState.get_state().crosshair_ratio.get()
    center_x, center_y = crosshair_ratio[0]* w, crosshair_ratio[1]* h
    crosshair_position = (center_x, center_y)
    TargetSelectorState.get_state().crosshair_position.set(crosshair_position)

    selected_target_bbox, selected_target_id = get_target_selector().target_selector(
        yolo_results,
        crosshair_position, 
    )
    TargetSelectorState.get_state().selected_target_bbox.set(selected_target_bbox)
    TargetSelectorState.get_state().selected_target_id.set(selected_target_id)
    pass


# 选择目标中心点
def calculate_target_vector(selected_target_bbox: Boxes):
    if not selected_target_bbox:
        return

    crosshair_position = TargetSelectorState.get_state().crosshair_position.get()

    # 计算目标点位置
    target_point_ratio = TargetSelectorState.get_state().target_point_ratio.get()
    target_point_x = selected_target_bbox.x1 + target_point_ratio[0] * (selected_target_bbox.x2 - selected_target_bbox.x1)
    target_point_y = selected_target_bbox.y1 + target_point_ratio[1] * (selected_target_bbox.y2 - selected_target_bbox.y1)

    # 计算向量
    vector_x = target_point_x - crosshair_position[0]
    vector_y = target_point_y - crosshair_position[1]

    TargetSelectorState.get_state().target_vector.set((vector_x, vector_y))
    
    pass