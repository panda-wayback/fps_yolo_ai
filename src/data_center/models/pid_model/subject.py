"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.pid_model.state_model import PIDModelState
from data_center.models.pid_model.subject_model import PIDSubjectModel
from data_center.models.pid_model.subjects.config import set_pid_config
from data_center.models.pid_model.subjects.last_output import set_last_output
from data_center.models.pid_model.subjects.pid_update import handle_pid_update
from singleton_classes.pid_controller.pid_controller import PIDController


class PIDSubject:
    """PID模型订阅统一接口"""
    
    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        PIDSubjectModel.config_subject.on_next(PIDModelState(kp=kp, ki=ki, kd=kd))
    
    @staticmethod
    def send_update(vector: tuple[float, float], dt=0.02):
        """发送更新"""
        PIDSubjectModel.update_subject.on_next((vector, dt))

    @staticmethod
    def send_output(output: tuple[float, float], error: tuple[float, float]):
        """发送输出"""
        PIDSubjectModel.output_subject.on_next((output, error))





def init_config_subject():
    """
    初始化PID模型状态的BehaviorSubject
    """
    PIDSubjectModel.config_subject.subscribe(set_pid_config)

    PIDSubjectModel.config_subject.subscribe(PIDController().set_pid_parameters)


def init_last_output_subject():
    """
    初始化last_output的BehaviorSubject
    """
    PIDSubjectModel.output_subject.subscribe(set_last_output)

def init_pid_update_subject():
    PIDSubjectModel.update_subject.subscribe(handle_pid_update)


def init_pid_subject_model():

    init_config_subject()
    init_pid_update_subject()
    init_last_output_subject()

init_pid_subject_model()