"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.index import get_data_center
from data_center.models.pid_model.model import PIDModel


class PIDModelState:
    """PID模型订阅统一接口"""
    @staticmethod
    def get_state() -> PIDModel:
        """获取状态"""
        return get_data_center().state.pid_model_state


    @staticmethod
    def init_subscribes():
        from data_center.models.pid_model.subscribes.send_mouse_driver import send_mouse_driver
        PIDModelState.get_state().output.subscribe(send_mouse_driver)
        pass

# init subscribes
PIDModelState.init_subscribes()
    
if __name__ == "__main__":
    pass