


from rx.subject import Subject
from data_center.index import get_data_center
from data_center.models.pid_model.state import PIDModelState
from singleton_classes.pid_controller.pid_controller import PIDController

# 创建PID模型状态的BehaviorSubject
subject = Subject()

def use_subject_pid_config(kp: float, ki: float, kd: float):
    """
    使用PID模型状态的BehaviorSubject
    """
    print(f"使用PID模型状态: kp={kp}, ki={ki}, kd={kd}")
    subject.on_next(PIDModelState(kp=kp, ki=ki, kd=kd))


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
    subject.subscribe(set_pid_config)

    subject.subscribe(PIDController().set_pid_parameters)

init_subject()
    

if __name__ == "__main__":
    use_subject_pid_config(1.0, 0.0, 0.0)