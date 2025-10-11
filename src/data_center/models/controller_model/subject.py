"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.controller_model.state import ControllerModelState  
from singleton_classes.controller.pid_controller import get_pid_controller


class ControllerSubject:
    
    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        ControllerModelState.get_state().kp.set(kp)
        ControllerModelState.get_state().ki.set(ki)
        ControllerModelState.get_state().kd.set(kd)
        # 设置PID参数
        get_pid_controller().set_pid_parameters(kp, ki, kd)

    @staticmethod
    def send_update(vector: tuple[float, float], dt: float = 0.02):
        """发送更新"""
        print(f"✅ {vector}  {dt}  PIDModel")
        output, error = get_pid_controller().get_vector_pid_res(vector, dt)
        print(f"✅ {vector}  {output}  {error}  PIDModel")
        ControllerModelState.get_state().output.set(output)
        ControllerModelState.get_state().error.set(error)
        pass


if __name__ == "__main__":
    ControllerSubject.send_config(1, 2, 3)