"""
鼠标向量话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.mouse_driver_model.subject_model import MouseDriverSubjectModel
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


def submit_vector(vector: tuple[float, float]):
    """执行鼠标模拟器提交向量"""
    try:
        get_mouse_simulator().submit_vector(vector)
        print(f"✅ 鼠标向量已提交: vx={vector[0]}, vy={vector[1]}")
    except Exception as e:
        print(f"❌ 鼠标向量提交失败: {e}")


def update_data_center_vector(vector: tuple[float, float]):
    """更新数据中心向量状态"""
    try:
        state = get_data_center().state.mouse_driver_state
        state.vx = vector[0]
        state.vy = vector[1]
        print(f"✅ 数据中心向量状态已更新: vx={vector[0]}, vy={vector[1]}")
    except Exception as e:
        print(f"❌ 数据中心向量状态更新失败: {e}")


def init_vector_subject():
    """初始化鼠标向量订阅"""
    MouseDriverSubjectModel.vector_subject.subscribe(submit_vector)
    MouseDriverSubjectModel.vector_subject.subscribe(update_data_center_vector)


init_vector_subject()


if __name__ == "__main__":
    # 测试用例
    MouseDriverSubjectModel.vector_subject.on_next((1.0, 1.0))