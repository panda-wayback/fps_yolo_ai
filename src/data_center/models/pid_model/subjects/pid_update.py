
from rx.subject import Subject

from singleton_classes.pid_controller.pid_controller import get_pid_controller

subject = Subject()

def use_subject_pid_update(vector: tuple[float, float], dt=0.02):
    try:
        print(f"使用PID更新: vector={vector}, dt={dt}")
        subject.on_next((vector, dt))
    except Exception as e:
        print(f"使用PID更新错误: {e}")


def init_subject():
    def handle_pid_update(data):
        try:
            vector, dt = data
            get_pid_controller().get_vector_pid_res(vector, dt)
        except Exception as e:
            print(f"PID更新处理错误: {e}")
    
    subject.subscribe(handle_pid_update)

init_subject()