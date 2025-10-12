"""
YOLO模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import List
import numpy as np
from ultralytics.models import YOLO

from data_center.models.yolo_model.state import YoloModelState
from utils.logger.logger import log_time
from utils.yolo.utils import get_device

class YoloSubject:

    @staticmethod
    def send_model_path(model_path: str):
        """发送YOLO模型路径"""
        YoloModelState.get_state().model_path.set(model_path)
        model = YOLO(model_path, task='detect')  # 明确指定任务类型为检测
        # GPU 优化（建议启用以提升性能）
        try:
            device = get_device()
            model.to(device)
            print(f"✅ 模型已加载到: {device}")
        except Exception as e:
            print(f"⚠️ GPU加载失败，使用CPU: {e}")
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
            classes = YoloModelState.get_state().selected_class_ids.get()
            return YoloModelState.get_state().model.get().track(
                img,                    # 图片
                verbose=False,          # 是否打印详细信息
                persist=True,           # 持久化追踪
                classes=classes,        # 选中的类别ID列表
                half=True,              # 使用FP16半精度（快2倍，需GPU支持）
                conf=0.5,               # 置信度阈值（提高可减少检测数量）
                max_det=5,             # 最大检测数量（减少可加速）
                agnostic_nms=False,     # 类别无关NMS（False更快）
                )
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
    YoloSubject.send_model_path("CFV8S_640_SELL.onnx")
    print(YoloModelState.get_state().model.get().names)
    YoloSubject.send_detect(np.zeros((300, 400, 3), dtype=np.uint8))
    YoloSubject.send_selected_class_ids([0])
    print(YoloModelState.get_state().selected_class_ids.get())