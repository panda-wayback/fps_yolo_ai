"""
截图相关的统一接口
"""


from data_center.index import get_data_center
from data_center.models.screenshot.subjects.config import use_screenshot_config_subject
from data_center.models.screenshot.subjects.img_subject import use_subject_img


class ScreenshotSubject:
    """截图订阅统一接口"""
    
    @staticmethod
    def use_config(mouse_pos: tuple[int, int] = None, 
                   region_size: tuple[int, int] = None, 
                   fps: float = None):
        """使用截图配置"""
        use_screenshot_config_subject(mouse_pos, region_size, fps)
    
    @staticmethod
    def send_image(img):
        """发送图片到订阅"""
        use_subject_img(img)
    
    @staticmethod
    def get_state():
        """获取截图状态"""
        return  get_data_center().state.screenshot_state