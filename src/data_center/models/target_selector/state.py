"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.target_selector.subscribes.send_vector_to_pid import send_vector_to_pid

class TargetSelectorState:
    """目标选择器订阅统一接口"""
        
    @staticmethod
    def get_state():
        """获取目标选择器状态"""
        return get_data_center().state.target_selector_state

    @staticmethod
    def init_subscribes():
        """初始化目标选择器订阅"""
        TargetSelectorState.get_state().selected_target_point.subscribe( send_vector_to_pid )