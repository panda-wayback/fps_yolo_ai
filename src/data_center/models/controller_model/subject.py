"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.controller_model.state import ControllerModelState  
from singleton_classes.controller.controller import get_controller
from utils.logger.logger import get_logger


class ControllerSubject:
    
    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        pass

    @staticmethod
    def compute(vector: tuple[float, float], dt: float = 0.02):
        """发送更新"""
        output, error = get_controller().compute(vector, dt)
        get_logger().info(f"✅ {vector}  {output}  {error}  ControllerModel")
        ControllerModelState.get_state().output.set(output)
        ControllerModelState.get_state().error.set(error)
        pass


if __name__ == "__main__":
    ControllerSubject.compute((1, 2))