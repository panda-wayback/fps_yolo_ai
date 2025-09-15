from singleton_classes.data_center import DataCenter
from singleton_classes.screenshot_img.main import start_screenshot
from .component.img_display import get_img_display


def get_img_show_component():
    """
    创建图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    start_screenshot()
    img_display = get_img_display()
    
    # 传入函数，每次调用都会获取最新值
    def get_current_image():
        return DataCenter().get_state().screenshot_img
    
    img_display.bind_to_data_center(get_current_image)
    return img_display