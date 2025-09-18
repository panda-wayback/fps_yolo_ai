
from rx.subject import BehaviorSubject
from data_center.index import get_data_center
import numpy as np
from typing import List, Any, Optional, Dict, Tuple

from data_center.models.yolo_model.index import YoloModelState

# 定义YOLO检测结果的类型
YoloDetection = Dict[str, Any]  # 单个检测结果
YoloResults = List[YoloDetection]  # YOLO检测结果列表

subject = BehaviorSubject(None)
def get_yolo_result_subject():
    return subject

state = get_data_center().state.yolo_model_state

def set_result_subject(value: Optional[YoloResults] = None):
    """设置YOLO检测结果"""
    state.yolo_results = value

def detect_yolo_result(value: Optional[YoloResults] = None):
    """处理YOLO检测结果"""
    state.yolo_results = value

if __name__ == "__main__":
    subject.subscribe(set_result_subject)
    subject.on_next(YoloModelState(yolo_results=[1, 2, 3]))
