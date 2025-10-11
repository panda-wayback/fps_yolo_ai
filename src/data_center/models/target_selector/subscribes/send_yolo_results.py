from typing import List, Any

from data_center.models.target_selector.state import TargetSelectorState
from singleton_classes.target_selector.target_selector import get_target_selector

def send_yolo_results(yolo_results: List[Any]):
    if not yolo_results:
        return
    selected_target_point, selected_target_bbox, selected_target_id = get_target_selector().target_selector(yolo_results)
    TargetSelectorState.get_state().selected_target_point.set(selected_target_point)
    TargetSelectorState.get_state().selected_target_bbox.set(selected_target_bbox)
    TargetSelectorState.get_state().selected_target_id.set(selected_target_id)