from typing import Tuple
import numpy as np
from data_center.models.base_state import BaseState, ReactiveVar


# 默认配置常量（UI 和 Model 共享）
DEFAULT_REGION_SIZE = (650, 240)  # 默认截图区域大小 (width, height)
DEFAULT_FPS = 80                  # 默认帧率


class ScreenshotModel(BaseState):
    """截图状态管理类"""
    # 鼠标位置和截图区域
    mouse_pos: ReactiveVar[Tuple[int, int]] = (756, 509)    # 鼠标位置
    region: ReactiveVar[Tuple[int, int, int, int]] = None  # 截图区域 (x, y, width, height)
    region_size: ReactiveVar[Tuple[int, int]] = DEFAULT_REGION_SIZE  # 截图区域大小
    screen_center: ReactiveVar[Tuple[int, int]] = None    # 截图图片中心点
    
    # 图片数据
    screenshot_img: ReactiveVar[np.ndarray] = None    # 截图图片数据
    
    # 配置参数
    fps: ReactiveVar[float] = DEFAULT_FPS
    interval: ReactiveVar[float] = 1.0 / DEFAULT_FPS    # 截图间隔


if __name__ == "__main__":
    # 测试用例
    from data_center.models.screenshot.state import ScreenshotModelState
    print("interval", ScreenshotModelState.get_state().interval.get())
    ScreenshotModelState.get_state().interval.get()
    ScreenshotModelState.get_state().interval.set(1.0 / 1000)
    print(ScreenshotModelState.get_state().interval.get())