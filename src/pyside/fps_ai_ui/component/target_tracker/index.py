from .component.target_tracker_control import get_target_tracker_control


def get_target_tracker_component():
    """
    创建目标跟踪器控制组件
    
    Returns:
        QGroupBox: 目标跟踪器控制组件
    """
    return get_target_tracker_control()
