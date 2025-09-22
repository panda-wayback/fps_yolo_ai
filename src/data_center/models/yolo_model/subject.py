"""
YOLO模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Optional, List
import numpy as np
from data_center.index import get_data_center
from ultralytics import YOLO

from data_center.models.target_selector.subject import TargetSelectorSubject



class YoloSubject:

    """YOLO模型订阅统一接口"""
    @staticmethod
    def get_state():
        """获取YOLO模型状态"""
        return get_data_center().state.yolo_model_state
    
    @staticmethod
    def init_subscribes():
        """初始化YOLO模型订阅"""
        YoloSubject.get_state().yolo_results.subscribe(TargetSelectorSubject.send_yolo_results)

    @staticmethod
    def send_model_path(model_path: str):
        """发送YOLO模型路径"""
        YoloSubject.get_state().model_path.set(model_path)
        model = YOLO(model_path)
        YoloSubject.get_state().model.set(model)

        # 设置模型类别信息
        class_names = list(model.names.values())
        class_ids = list(model.names.keys())

        YoloSubject.get_state().class_names.set(class_names)
        YoloSubject.get_state().class_ids.set(class_ids)
    
    @staticmethod
    def send_detect(img: np.ndarray = None):
        """发送YOLO检测图片"""
        result = YoloSubject.get_state().model(img, verbose=False)
        YoloSubject.get_state().yolo_results.set(result)

    @staticmethod
    def send_selected_class_ids(selected_class_ids: List[int]):
        """发送选中的类别ID"""
        YoloSubject.get_state().selected_class_ids.set(selected_class_ids)


YoloSubject.init_subscribes()