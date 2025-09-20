


from data_center.index import get_data_center
from data_center.models.pid_model.state_model import PIDModelState


def set_pid_config(config: PIDModelState):
    """
    设置PID模型状态
    """
    print(f"设置PID模型状态: {config}")
    get_data_center().state.pid_model_state.merge_state(config)

