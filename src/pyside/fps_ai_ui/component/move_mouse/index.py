from .component.mouse_control import get_mouse_control


def get_move_mouse_component():
    """
    创建鼠标模拟器控制组件
    
    Returns:
        QGroupBox: 鼠标控制组件
    """
    return get_mouse_control()
