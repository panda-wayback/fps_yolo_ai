"""
YOLO模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Optional, List
from data_center.models.yolo_model.subject_model import YoloSubjectModel
import numpy as np
from data_center.models.yolo_model.subjects.detect_subject import set_detect_subject
from data_center.models.yolo_model.subjects.load_model import set_yolo_model_state_results
from data_center.models.yolo_model.subjects.result_subject import set_result_subject
from data_center.models.yolo_model.subjects.selected_class_subject import update_selected_class_ids



class YoloSubject:
    """YOLO模型订阅统一接口"""
    
    @staticmethod
    def send_model_path(model_path: str):
        """发送YOLO模型路径"""
        YoloSubjectModel.load_model_subject.on_next(model_path)
    
    @staticmethod
    def send_result(result: Optional[List] = None):
        """发送YOLO检测结果"""
        YoloSubjectModel.result_subject.on_next(result)
    
    @staticmethod
    def send_detect(img: np.ndarray = None):
        """发送YOLO检测图片"""
        YoloSubjectModel.detect_subject.on_next(img)
    
    @staticmethod
    def send_selected_class_ids(selected_class_ids: List[int]):
        """设置选中的类别ID"""
        YoloSubjectModel.selected_class_subject.on_next(selected_class_ids)
    
    @staticmethod
    def get_yolo_model_state():
        """获取YOLO模型状态"""
        from data_center.index import get_data_center
        return get_data_center().state.yolo_model_state



def init_detect_subject():
    """初始化YOLO检测订阅"""
    YoloSubjectModel.detect_subject.subscribe(set_detect_subject)

def init_load_model_subject():
    """初始化YOLO模型加载订阅"""
    YoloSubjectModel.load_model_subject.subscribe(set_yolo_model_state_results)

def init_result_subject():
    """初始化YOLO检测结果订阅"""
    YoloSubjectModel.result_subject.subscribe(set_result_subject)

def init_selected_class_subject():
    """初始化YOLO选中类别订阅"""
    YoloSubjectModel.selected_class_subject.subscribe(update_selected_class_ids)

def init_yolo_subject_model():
    """初始化YOLO所有话题绑定"""
    init_detect_subject()
    init_load_model_subject()
    init_result_subject()
    init_selected_class_subject()

init_yolo_subject_model()



