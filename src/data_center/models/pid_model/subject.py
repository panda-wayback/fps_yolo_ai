"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.index import get_data_center
from data_center.models.pid_model.state_model import PIDModelState
from singleton_classes.pid_controller.pid_controller import get_pid_controller


class PIDSubject:
    """PID模型订阅统一接口"""

    # init subscribes
    @staticmethod
    def init_subscribes():
        PIDSubject.get_state().kp.subscribe(lambda x: print(f"kp: {x}"))
        PIDSubject.get_state().ki.subscribe(lambda x: print(f"ki: {x}"))
        PIDSubject.get_state().kd.subscribe(lambda x: print(f"kd: {x}"))
        PIDSubject.get_state().output.subscribe(lambda x: print(f"output: {x}"))
        PIDSubject.get_state().error.subscribe(lambda x: print(f"error: {x}"))

        pass

    @staticmethod
    def get_state()->PIDModelState:
        """获取状态"""
        return get_data_center().state.pid_model_state

    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        PIDSubject.get_state().kp.set(kp)
        PIDSubject.get_state().ki.set(ki)
        PIDSubject.get_state().kd.set(kd)
        # 设置PID参数
        get_pid_controller().set_pid_parameters(kp, ki, kd)

    @staticmethod
    def send_update(vector: tuple[float, float], dt: float):
        """发送更新"""
        output, error = get_pid_controller().get_vector_pid_res(vector, dt)
        PIDSubject.get_state().output.set(output)
        PIDSubject.get_state().error.set(error)
        pass

PIDSubject.init_subscribes()

if __name__ == "__main__":
    PIDSubject.send_config(1, 2, 3)
    print(PIDSubject.get_state())