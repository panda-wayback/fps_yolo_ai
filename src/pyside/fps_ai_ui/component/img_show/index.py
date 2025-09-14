from .component.img_display import get_img_display


def get_img_show_component():
    """
    创建图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    return get_img_display()
