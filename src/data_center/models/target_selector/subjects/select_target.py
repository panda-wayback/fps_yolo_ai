from rx.subject import Subject
from data_center.index import get_data_center

from singleton_classes.target_selector.target_selector import get_target_selector

subject = Subject()

def use_target_select_subject(yolo_results=None):
    """使用目标选择订阅"""
    if yolo_results is None:
        return
    subject.on_next(yolo_results)

def set_target_select_subject(yolo_results=None):
    """设置目标选择结果"""
    if yolo_results is None:
        # 清空选择结果
        get_data_center().state.target_selector_state.update_state(
            selected_point=None,
            selected_bbox=None,
            selected_confidence=None,
            selected_class_id=None
        )
        return
    
    # 使用目标选择器进行选择（内部会自动获取配置）
    target = get_target_selector().target_selector(yolo_results)
    
    if target:
        selected_point = target['center']
        selected_bbox = target['bbox']
        selected_confidence = target['confidence']
        selected_class_id = target['class_id']
        
        get_data_center().state.target_selector_state.update_state(
            selected_point=selected_point,
            selected_bbox=selected_bbox,
            selected_confidence=selected_confidence,
            selected_class_id=selected_class_id
        )
    else:
        # 没有选中目标
        get_data_center().state.target_selector_state.update_state(
            selected_point=None,
            selected_bbox=None,
            selected_confidence=None,
            selected_class_id=None
        )

def init_target_select_subject():
    """初始化目标选择订阅"""
    subject.subscribe(set_target_select_subject)
    
    # 订阅YOLO检测结果
    try:
        from data_center.models.yolo_model.subjects.result_subject import subject as yolo_result_subject
        yolo_result_subject.subscribe(use_target_select_subject)
        print("✅ 目标选择器已订阅YOLO检测结果")
    except ImportError as e:
        print(f"⚠️ 无法订阅YOLO检测结果: {e}")

init_target_select_subject()
