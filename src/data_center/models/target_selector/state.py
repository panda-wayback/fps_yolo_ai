"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from data_center.index import get_data_center


class TargetSelectorState:
    """目标选择器订阅统一接口"""
        
    @staticmethod
    def get_state():
        """获取目标选择器状态"""
        return get_data_center().state.target_selector_state

    @staticmethod
    def init_subscribes():
        """初始化目标选择器订阅"""
        from data_center.models.target_selector.subscribes.send_yolo_results import send_yolo_results
        TargetSelectorState.get_state().yolo_results.subscribe(send_yolo_results)
        
        from data_center.models.controller_model.subject import  ControllerSubject
        TargetSelectorState.get_state().selected_target_point.subscribe(ControllerSubject.compute)

        from data_center.models.controller_model.subject import  ControllerSubject
        TargetSelectorState.get_state().selected_target_id.subscribe(ControllerSubject.update_target_id)

        pass