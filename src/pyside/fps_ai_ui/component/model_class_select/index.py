from .component.class_selector import get_class_selector

def get_model_class_selector():
    """
    获取模型类别选择组件
    
    Returns:
        QGroupBox: 模型类别选择组件
    """
    return get_class_selector()
