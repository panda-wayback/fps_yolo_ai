from typing import Optional, Tuple
import numpy as np
from pydantic import ConfigDict
from data_center.models.base_state import BaseState, ReactiveVar


class ScreenshotModel(BaseState):
    """截图状态管理类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # 鼠标位置和截图区域
    mouse_pos: ReactiveVar[Tuple[int, int]] = None    # 鼠标位置
    region: ReactiveVar[Tuple[int, int, int, int]] = None  # 截图区域 (x, y, width, height)
    region_size: ReactiveVar[Tuple[int, int]] = None  # 截图区域大小 (width, height)
    screen_center: ReactiveVar[Tuple[int, int]] = None    # 截图图片中心点
    
    # 图片数据
    screenshot_img: ReactiveVar[np.ndarray] = None    # 截图图片数据
    
    # 配置参数
    fps: ReactiveVar[float] = 1000
    interval: ReactiveVar[float] = 1.0 / 1000    # 截图间隔
