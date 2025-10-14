from typing import List, Any

from data_center.models.target_selector.state import TargetSelectorState
from data_center.models.yolo_model.state import YoloModelState
from singleton_classes.target_selector.target_selector import get_target_selector

def send_yolo_results(yolo_results: List[Any]):
    if not yolo_results:
        return
    crosshair_offset_vector = YoloModelState.get_state().crosshair_offset_vector.get()
    selected_target_point, selected_target_bbox, selected_target_id = get_target_selector().target_selector(yolo_results, crosshair_offset_vector)
    TargetSelectorState.get_state().selected_target_point.set(selected_target_point)
    TargetSelectorState.get_state().selected_target_bbox.set(selected_target_bbox)
    TargetSelectorState.get_state().selected_target_id.set(selected_target_id)