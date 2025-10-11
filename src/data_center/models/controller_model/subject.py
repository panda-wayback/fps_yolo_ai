"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.controller_model.state import ControllerModelState  
from singleton_classes.controller.controller import get_controller
from utils.logger.logger import get_logger


class ControllerSubject:
    
    @staticmethod
    def send_config(order: int, sample_time: float, b0: float, w_cl: float, k_eso: float, output_limits: tuple[float, float], rate_limits: tuple[float, float]):
        """使用PID配置"""
        ControllerModelState.get_state().order.set(order)
        ControllerModelState.get_state().sample_time.set(sample_time)
        ControllerModelState.get_state().b0.set(b0)
        ControllerModelState.get_state().w_cl.set(w_cl)
        ControllerModelState.get_state().k_eso.set(k_eso)
        ControllerModelState.get_state().output_limits.set(output_limits)
        ControllerModelState.get_state().rate_limits.set(rate_limits)
        get_controller().set_config(order=order, sample_time=sample_time, b0=b0, w_cl=w_cl, k_eso=k_eso, output_limits=output_limits, rate_limits=rate_limits)

    @staticmethod
    def compute(vector: tuple[float, float]):
        """发送更新"""
        output = get_controller().compute(vector)
        get_logger().info(f"✅ {vector}  {output}  ControllerModel")
        ControllerModelState.get_state().output.set(output)
        ControllerModelState.get_state().error.set(vector)
        pass

    @staticmethod
    def update_target_id(target_id: int):
        """更新目标ID"""
        get_controller().update_target_id(target_id)



if __name__ == "__main__":
    ControllerSubject.compute((1, 2))