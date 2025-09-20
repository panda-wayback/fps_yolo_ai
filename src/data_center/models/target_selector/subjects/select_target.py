"""
目标选择话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.pid_model.subject import PIDSubject
from singleton_classes.target_selector.target_selector import get_target_selector


def set_target_select_subject(yolo_results=None):
    # 使用目标选择器进行选择（内部会自动获取配置）
    try:
        selected_point, selected_bbox, selected_confidence, selected_class_id  = get_target_selector().target_selector(yolo_results)
        get_data_center().state.target_selector_state.update_state(
                selected_point=selected_point,
                selected_bbox=selected_bbox,
                selected_confidence=selected_confidence,
                selected_class_id=selected_class_id
            )
        # 发送更新
        PIDSubject.send_update(selected_point)
    except Exception as e:
        print(f"❌ 目标选择错误: {e}")



if __name__ == "__main__":
    # 测试用例
    from data_center.models.target_selector.subject import TargetSelectorSubject
    TargetSelectorSubject.send_yolo_results(None)