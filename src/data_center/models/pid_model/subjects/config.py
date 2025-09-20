


from data_center.index import get_data_center
from data_center.models.pid_model.state_model import PIDModelState
from singleton_classes.pid_controller.pid_controller import PIDController


def set_pid_config(config: PIDModelState):
    """
    设置PID模型状态
    """
    print(f"设置PID模型状态: {config}")
    get_data_center().state.pid_model_state.merge_state(config)
    PIDController().set_pid_parameters(config.kp, config.ki, config.kd)

