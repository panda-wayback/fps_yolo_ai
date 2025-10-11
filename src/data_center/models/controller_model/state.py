"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.index import get_data_center
from data_center.models.controller_model.model import ControllerModel


class ControllerModelState:
    """Controller模型订阅统一接口"""
    @staticmethod
    def get_state() -> ControllerModel:
        """获取状态"""
        return get_data_center().state.controller_model_state


    @staticmethod
    def init_subscribes():
        from data_center.models.controller_model.subscribes.send_mouse_driver import send_mouse_driver
        ControllerModelState.get_state().output.subscribe(send_mouse_driver)
        pass

    
if __name__ == "__main__":
    pass