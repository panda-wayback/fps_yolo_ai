"""
截图模型相关的统一接口
基于PID模型的最佳实践
"""

from typing import Tuple, Optional
import numpy as np
from data_center.models.screenshot.state_model import ScreenshotState
from data_center.models.screenshot.subject_model import ScreenshotSubjectModel
from data_center.models.screenshot.subjects.config import set_screenshot_state_settings
from data_center.models.screenshot.subjects.img_subject import on_img_change, detect_img


class ScreenshotSubject:
    """截图订阅统一接口"""
    
    @staticmethod
    def use_config(
        mouse_pos: Optional[Tuple[int, int]] = None,
        region_size: Optional[Tuple[int, int]] = None,
        fps: Optional[float] = None
    ):
        """使用截图配置"""
        config_data = {}
        if mouse_pos is not None:
            config_data['mouse_pos'] = mouse_pos
        if region_size is not None:
            config_data['region_size'] = region_size
        if fps is not None:
            config_data['fps'] = fps
        
        config = ScreenshotState(**config_data)
        ScreenshotSubjectModel.config_subject.on_next(config)
    
    @staticmethod
    def send_image(img: np.ndarray):
        """发送图片到订阅"""
        ScreenshotSubjectModel.img_subject.on_next(img)
    
    @staticmethod
    def get_state():
        """获取截图状态"""
        from data_center.index import get_data_center
        return get_data_center().state.screenshot_state

def init_config_subject():
    """初始化截图配置订阅"""
    ScreenshotSubjectModel.config_subject.subscribe(set_screenshot_state_settings)


def init_img_subject():
    """初始化截图图片订阅"""
    # 订阅图片变化 - 使用独立线程确保并行处理
    ScreenshotSubjectModel.img_subject.subscribe(on_img_change)  # 图片保存 - 轻量级任务
    ScreenshotSubjectModel.img_subject.subscribe(detect_img)     # YOLO检测 - 重量级任务
    print("✅ 截图图片订阅初始化成功")


def init_screenshot_subject_model():
    """初始化截图所有话题绑定"""
    init_config_subject()
    init_img_subject()


init_screenshot_subject_model()
