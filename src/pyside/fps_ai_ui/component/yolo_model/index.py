from .component.yolo_model_selector import get_yolo_model_selector


def get_yolo_model_component():
    """
    创建YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    return get_yolo_model_selector()