"""
PID模型相关的统一接口
"""


# 延迟导入，避免循环导入


class PIDSubject:
    """PID模型订阅统一接口"""
    
    @staticmethod
    def send_config(kp: float, ki: float, kd: float):
        """使用PID配置"""
        from data_center.models.pid_model.subjects.config import use_subject_pid_config
        use_subject_pid_config(kp, ki, kd)
    
    @staticmethod
    def send_update(vector: tuple[float, float], dt=0.02):
        """发送更新"""
        from data_center.models.pid_model.subjects.pid_update import use_subject_pid_update
        use_subject_pid_update(vector, dt)

    @staticmethod
    def send_output(output: tuple[float, float], error: tuple[float, float]):
        """发送输出"""
        from data_center.models.pid_model.subjects.last_output import use_subject_last_output
        use_subject_last_output(output, error)
