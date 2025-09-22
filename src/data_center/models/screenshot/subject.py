"""
截图模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Tuple, Optional
import numpy as np
from data_center.models.screenshot.subjects.config import get_screenshot_state_settings
from data_center.models.screenshot.subjects.screenshot_img import on_screenshot_img


class ScreenshotSubject:
    """截图订阅统一接口"""

    @staticmethod
    def get_state():
        """获取截图状态"""
        from data_center.index import get_data_center
        return get_data_center().state.screenshot_state
    
    @staticmethod
    def init_subscribes():
        """初始化截图订阅"""
        ScreenshotSubject.get_state().screenshot_img.subscribe(on_screenshot_img)

    @staticmethod
    def send_config(
        mouse_pos: Optional[Tuple[int, int]] = None,
        region_size: Optional[Tuple[int, int]] = None,
        fps: Optional[float] = None
    ):
        # 设置截图状态
        ScreenshotSubject.get_state().mouse_pos.set(mouse_pos)
        ScreenshotSubject.get_state().region_size.set(region_size)
        ScreenshotSubject.get_state().fps.set(fps)

        # 设置截图区域和中心点
        region, screen_center, interval = get_screenshot_state_settings(mouse_pos, region_size, fps)
        ScreenshotSubject.get_state().region.set(region)
        ScreenshotSubject.get_state().screen_center.set(screen_center)
        ScreenshotSubject.get_state().interval.set(interval)

        pass

    
    @staticmethod
    def send_image(img: np.ndarray):
        """发送图片到订阅"""
        ScreenshotSubject.get_state().screenshot_img.set(img)
    

