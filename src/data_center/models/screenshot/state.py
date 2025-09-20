from typing import Optional, Tuple
import numpy as np
from data_center.models.base_state import BaseState


class ScreenshotState(BaseState):
    """截图状态管理类"""
    mouse_pos: Optional[Tuple[int, int]] = None    # 鼠标位置
    # 截图区域 def capture_screenshot(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    region: Optional[Tuple[int, int, int, int]] = None
    region_size: Optional[Tuple[int, int]] = None           # 截图区域大小 (width, height)
    screen_center: Optional[Tuple[int, int]] = None    # 截图图片中心点
    screenshot_img: Optional[np.ndarray] = None        # 截图图片数据
    fps: Optional[float] = None    # 截图帧率
    marked_img: Optional[np.ndarray] = None        # 标记过目标的图片