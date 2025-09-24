"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.pid_model.state import PIDModelState
from singleton_classes.pid_controller.pid_controller import get_pid_controller


class PIDSubject:
    
    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        PIDModelState.get_state().kp.set(kp)
        PIDModelState.get_state().ki.set(ki)
        PIDModelState.get_state().kd.set(kd)
        # 设置PID参数
        get_pid_controller().set_pid_parameters(kp, ki, kd)

    @staticmethod
    def send_update(vector: tuple[float, float], dt: float = 0.02):
        """发送更新"""
        output, error = get_pid_controller().get_vector_pid_res(vector, dt)
        PIDModelState.get_state().output.set(output)
        PIDModelState.get_state().error.set(error)
        pass


if __name__ == "__main__":
    PIDSubject.send_config(1, 2, 3)