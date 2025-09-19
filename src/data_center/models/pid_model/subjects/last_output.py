"""
该模块用于记录PID模型的上一次输出结果（last_output）。
"""

from rx.subject import Subject
from data_center.index import get_data_center

# 创建last_output的Subject
last_output_subject = Subject()

def get_pid_model_last_output_subject():
    """
    获取last_output的BehaviorSubject
    """
    return last_output_subject

def set_last_output(params: tuple[tuple[float, float], tuple[float, float]]):
    """
    设置上一次PID输出结果
    """
    try:
        output, error = params
        
        print(f"记录PID上一次输出: x={output[0]}, y={output[1]}")
        # 更新数据中心中的状态
        get_data_center().state.pid_model_state.last_output_x = output[0]
        get_data_center().state.pid_model_state.last_output_y = output[1]
        get_data_center().state.pid_model_state.last_error_x = error[0]
        get_data_center().state.pid_model_state.last_error_y = error[1]
    except Exception as e:
        print(f"设置上一次PID 结果失败: {e}")


def use_subject_last_output(output: tuple[float, float] , error: tuple[float, float]):
    """
    使用last_output的BehaviorSubject
    """
    try:
        last_output_subject.on_next((output, error))
    except Exception as e:
        print(f"使用last_output的BehaviorSubject错误: {e}")

def init_last_output_subject():
    """
    初始化last_output的BehaviorSubject
    """
    last_output_subject.subscribe(set_last_output)


init_last_output_subject()
