"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.auto_attack_model.subject import AutoAttackSubject
from utils.thread.main import threaded


class TargetSelectorState:
    """目标选择器订阅统一接口"""
        
    @staticmethod
    def get_state():
        """获取目标选择器状态"""
        return get_data_center().state.target_selector_state

    @staticmethod
    def init_subscribes():

        """初始化目标选择器订阅"""
        from data_center.models.target_selector.subscribes.select_target import select_target, calculate_target_vector
        # 订阅YOLO检测结果
        TargetSelectorState.get_state().yolo_results.subscribe(select_target)
        # 订阅选中目标边框
        TargetSelectorState.get_state().selected_target_bbox.subscribe(calculate_target_vector)

        from data_center.models.controller_model.subject import  ControllerSubject
        # 订阅距离目标的向量
        TargetSelectorState.get_state().target_vector.subscribe(ControllerSubject.compute)
        # 订阅更新目标ID
        TargetSelectorState.get_state().target_vector.subscribe(
            threaded(AutoAttackSubject.update_track_point)
        )

        from data_center.models.controller_model.subject import  ControllerSubject
        # 订阅更新目标ID
        TargetSelectorState.get_state().selected_target_id.subscribe(ControllerSubject.update_target_id)

        pass