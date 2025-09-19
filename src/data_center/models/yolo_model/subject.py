

from typing import Optional
from data_center.models.yolo_model.subjects.detect_subject import use_yolo_detect_subject
from data_center.models.yolo_model.subjects.result_subject import YoloResults, use_yolo_result_subject
from data_center.models.yolo_model.subjects.state import use_yolo_model_state_subject
import numpy as np


class YoloSubject:
    """YOLO模型订阅统一接口"""
    
    @staticmethod
    def send_model(model_path: str):
        """使用YOLO模型"""
        use_yolo_model_state_subject(model_path)
    
    @staticmethod
    def send_result(result: Optional[YoloResults] = None):
        """发送YOLO检测结果"""
        use_yolo_result_subject(result)
    
    @staticmethod
    def send_detect(img:np.ndarray = None):
        """发送YOLO检测图片"""
        use_yolo_detect_subject(img)