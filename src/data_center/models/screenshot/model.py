from typing import Optional, Tuple
import numpy as np
from pydantic import ConfigDict
from data_center.models.base_state import BaseState, ReactiveVar



class ScreenshotModel(BaseState):
    """截图状态管理类"""
    # 鼠标位置和截图区域
    is_running: ReactiveVar[bool] = None    # 是否正在截图
    mouse_pos: ReactiveVar[Tuple[int, int]] = None    # 鼠标位置
    region: ReactiveVar[Tuple[int, int, int, int]] = None  # 截图区域 (x, y, width, height)
    region_size: ReactiveVar[Tuple[int, int]] = None  # 截图区域大小 (width, height)
    screen_center: ReactiveVar[Tuple[int, int]] = None    # 截图图片中心点
    
    # 图片数据
    screenshot_img: ReactiveVar[np.ndarray] = None    # 截图图片数据
    
    # 配置参数
    fps: ReactiveVar[float] = 1000
    interval: ReactiveVar[float] = 1.0 / 1000    # 截图间隔


if __name__ == "__main__":
    # 测试用例
    from data_center.models.screenshot.state import ScreenshotModelState
    print("interval", ScreenshotModelState.get_state().interval.get())
    ScreenshotModelState.get_state().interval.get()
    ScreenshotModelState.get_state().interval.set(1.0 / 2000)
    print(ScreenshotModelState.get_state().interval.get())