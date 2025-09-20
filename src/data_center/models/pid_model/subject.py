"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


from data_center.models.pid_model.state_model import PIDModelState
from data_center.models.pid_model.subject_model import PIDSubjectModel


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
