"""
鼠标驱动模型相关的统一接口
基于PID模型的最佳实践
"""
from data_center.index import get_data_center
from data_center.models.mouse_driver_model.subjects.send_vector import submit_vector

class MouseDriverState:
    """鼠标驱动模型订阅统一接口"""
    
    @staticmethod
    def get_state():
        """获取鼠标驱动状态"""
        return get_data_center().state.mouse_driver_state


    @staticmethod
    def init_subscribes():
        MouseDriverState.get_state().vector.subscribe(
            submit_vector
        )
        pass

MouseDriverState.init_subscribes()