"""
目标选择话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.target_selector.subject_model import TargetSelectorSubjectModel
from singleton_classes.target_selector.target_selector import get_target_selector


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
    try:
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
    except Exception as e:
        print(f"❌ 目标选择错误: {e}")


def init_select_subject():
    """初始化目标选择订阅"""
    TargetSelectorSubjectModel.select_subject.subscribe(set_target_select_subject)


init_select_subject()


if __name__ == "__main__":
    # 测试用例
    TargetSelectorSubjectModel.select_subject.on_next(None)