from typing import Optional, Tuple
import numpy as np
from pydantic import ConfigDict
from data_center.models.base_state import BaseState


class ScreenshotState(BaseState):
    """截图状态管理类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # 鼠标位置和截图区域
    mouse_pos: Optional[Tuple[int, int]] = None    # 鼠标位置
    region: Optional[Tuple[int, int, int, int]] = None  # 截图区域 (x, y, width, height)
    region_size: Optional[Tuple[int, int]] = None  # 截图区域大小 (width, height)
    screen_center: Optional[Tuple[int, int]] = None    # 截图图片中心点
    
    # 图片数据
    screenshot_img: Optional[np.ndarray] = None    # 截图图片数据
    marked_img: Optional[np.ndarray] = None        # 标记过目标的图片
    
    # 配置参数
    fps: Optional[float] = None    # 截图帧率
