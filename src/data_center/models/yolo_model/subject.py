

from typing import Optional

from data_center.models.yolo_model.subjects.detect_subject import use_yolo_detect_subject
from data_center.models.yolo_model.subjects.result_subject import YoloResults, use_yolo_result_subject
from data_center.models.yolo_model.subjects.load_model import use_yolo_model_path_subject
from data_center.models.yolo_model.subjects.selected_class_subject import use_yolo_selected_class_subject
import numpy as np
from typing import List


class YoloSubject:
    """YOLO模型订阅统一接口"""
    
    @staticmethod
    def send_model_path(model_path: str):
        """使用YOLO模型"""
        use_yolo_model_path_subject(model_path)
    
    @staticmethod
    def send_result(result: Optional[YoloResults] = None):
        """发送YOLO检测结果"""
        use_yolo_result_subject(result)
    
    @staticmethod
    def send_detect(img:np.ndarray = None):
        """发送YOLO检测图片"""
        use_yolo_detect_subject(img)
    
    @staticmethod
    def send_selected_class_ids(selected_class_ids: List[int]):
        """设置选中的类别ID"""
        use_yolo_selected_class_subject(selected_class_ids)
    
    @staticmethod # get yolo model state
    def get_yolo_model_state():
        """获取YOLO模型状态"""
        from data_center.index import get_data_center
        return get_data_center().state.yolo_model_state