

from typing import Optional

from data_center.models.yolo_model.subjects.detect_subject import use_yolo_detect_subject
from data_center.models.yolo_model.subjects.result_subject import YoloResults, use_yolo_result_subject
from data_center.models.yolo_model.subjects.config import use_yolo_model_path_subject
import numpy as np


class YoloSubject:
    """YOLO模型订阅统一接口"""
    
    @staticmethod
    def send_model_path(model_path: str):
        """使用YOLO模型"""
        use_yolo_model_path_subject(model_path)
    
    @staticmethod
    def send_result(result: Optional[YoloResults] = None, current_time: float = None):
        """发送YOLO检测结果"""
        use_yolo_result_subject(result, current_time)
    
    @staticmethod
    def send_detect(img:np.ndarray = None):
        """发送YOLO检测图片"""
        use_yolo_detect_subject(img)
    
    @staticmethod # get yolo model state
    def get_yolo_model_state():
        """获取YOLO模型状态"""
        from data_center.index import get_data_center
        return get_data_center().state.yolo_model_state