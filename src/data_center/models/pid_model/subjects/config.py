


from rx.subject import Subject
from data_center.index import get_data_center
from data_center.models.pid_model.state_model import PIDModelState
from data_center.models.pid_model.subject_model import PIDSubjectModel
from singleton_classes.pid_controller.pid_controller import PIDController


def set_pid_config(config: PIDModelState):
    """
    设置PID模型状态
    """
    print(f"设置PID模型状态: {config}")
    get_data_center().state.pid_model_state.merge_state(config)


def init_subject():
    """
    初始化PID模型状态的BehaviorSubject
    """
    PIDSubjectModel.config_subject.subscribe(set_pid_config)

    PIDSubjectModel.config_subject.subscribe(PIDController().set_pid_parameters)

init_subject()
    

if __name__ == "__main__":
    PIDSubjectModel.config_subject.on_next(PIDModelState(kp=1.0, ki=0.0, kd=0.0))