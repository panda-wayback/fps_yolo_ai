"""
YOLO模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import List
import numpy as np
from ultralytics import YOLO

from data_center.models.yolo_model.state import YoloModelState
from utils.logger.logger import log_time

class YoloSubject:

    @staticmethod
    def send_model_path(model_path: str):
        """发送YOLO模型路径"""
        YoloModelState.get_state().model_path.set(model_path)
        model = YOLO(model_path)
        YoloModelState.get_state().model.set(model)

        # 设置模型类别信息
        class_names = list(model.names.values())
        class_ids = list(model.names.keys())

        YoloModelState.get_state().class_names.set(class_names)
        YoloModelState.get_state().class_ids.set(class_ids)
    
    @staticmethod
    def send_detect(img: np.ndarray = None):
        """发送YOLO检测图片"""
        if img is None:
            return
        @log_time
        def yolo_detect():
            return YoloModelState.get_state().model.get()(img, verbose=False)
        result = yolo_detect()
        YoloModelState.get_state().yolo_results.set(result)
        YoloModelState.get_state().marked_img.set(result[0].plot())

    @staticmethod
    def send_selected_class_ids(selected_class_ids: List[int]):
        """发送选中的类别ID"""
        YoloModelState.get_state().selected_class_ids.set(selected_class_ids)


if __name__ == "__main__":
    # 测试用例
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_model_path("runs/aimlab_fast/weights/best.pt")
    print(YoloModelState.get_state().model.get().names)
    YoloSubject.send_detect(np.zeros((300, 400, 3), dtype=np.uint8))
    YoloSubject.send_selected_class_ids([0])
    print(YoloModelState.get_state().selected_class_ids.get())