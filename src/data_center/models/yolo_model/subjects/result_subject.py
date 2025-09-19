
from rx.subject import BehaviorSubject
from data_center.index import get_data_center
import numpy as np
from typing import List, Any, Optional, Dict, Tuple

from data_center.models.yolo_model.state import YoloModelState

# 定义YOLO检测结果的类型
YoloDetection = Dict[str, Any]  # 单个检测结果
YoloResults = List[YoloDetection]  # YOLO检测结果列表

subject = BehaviorSubject(None)

def use_yolo_result_subject(img:np.ndarray = None, value: Optional[YoloResults] = None):
    subject.on_next(value)

state = get_data_center().state.yolo_model_state

def set_result_subject(value: Optional[YoloResults] = None):
    """设置YOLO检测结果"""
    try:
        state.yolo_results = value
        state.marked_img = value.plot()
    except Exception as e:
        print(f"设置YOLO检测结果错误: {e}")

def init_yolo_result_subject():
    """初始化YOLO检测结果订阅"""
    subject.subscribe(set_result_subject)

init_yolo_result_subject()

if __name__ == "__main__":
    subject.subscribe(set_result_subject)
    subject.on_next(YoloModelState(yolo_results=[1, 2, 3]))
