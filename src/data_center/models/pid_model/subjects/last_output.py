"""
该模块用于记录PID模型的上一次输出结果（last_output）。
"""
from data_center.index import get_data_center
from data_center.models.pid_model.subject_model import PIDSubjectModel


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


def init_last_output_subject():
    """
    初始化last_output的BehaviorSubject
    """
    PIDSubjectModel.output_subject.subscribe(set_last_output)


init_last_output_subject()
