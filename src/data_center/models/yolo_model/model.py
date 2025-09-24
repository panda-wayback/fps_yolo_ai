from typing import Any, List, Optional
from pydantic import ConfigDict
import numpy as np
from ultralytics import YOLO
from data_center.models.base_state import BaseState, ReactiveVar


class YoloModel(BaseState):
    """YOLO模型状态类"""

    model: ReactiveVar[YOLO] = None  
    model_path: ReactiveVar[str] = ""               # 当前加载的模型路径
    class_names: ReactiveVar[List[str]] = []  # 模型的所有类别名称
    class_ids: ReactiveVar[List[int]] = []    # 模型的所有类别ID
    selected_class_ids: ReactiveVar[List[int]] = [] # 当前选择的要识别的类别ID
    marked_img: ReactiveVar[np.ndarray] = None        # 标记过目标的图片
    yolo_results: ReactiveVar[List[Any]] = None       # YOLO模型输出

