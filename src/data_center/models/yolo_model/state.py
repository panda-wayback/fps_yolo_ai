from typing import Any
from typing_extensions import List, Optional
from pydantic import ConfigDict
import numpy as np
from data_center.models.base_state import BaseState
from ultralytics import YOLO

class YoloModelState(BaseState):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    model: Optional[YOLO] = None
    model_path: Optional[str] = None               # 当前加载的模型路径
    model_class_names: Optional[List[str]] = None  # 模型的所有类别名称
    model_class_ids: Optional[List[int]] = None    # 模型的所有类别ID
    selected_class_ids: Optional[List[int]] = None # 当前选择的要识别的类别ID
    marked_img: Optional[np.ndarray] = None        # 标记过目标的图片
    yolo_results: Optional[List[Any]] = None       # YOLO模型输出


