"""
截图模型相关的统一接口
基于PID模型的最佳实践
"""
from data_center.index import get_data_center
from data_center.models.screenshot.subjects.screenshot_img import on_screenshot_img


class ScreenshotModelState:
    """截图订阅统一接口"""

    @staticmethod
    def get_state():
        """获取截图状态"""
        
        return get_data_center().state.screenshot_state
    
    @staticmethod
    def init_subscribes():
        """初始化截图订阅"""
        ScreenshotModelState.get_state().screenshot_img.subscribe(on_screenshot_img)


ScreenshotModelState.init_subscribes()