
from data_center.models.pid_model.subject import PIDSubject
from singleton_classes.pid_controller.pid_controller import get_pid_controller



def handle_pid_update(data):
    try:
        vector, dt = data
        output, error = get_pid_controller().get_vector_pid_res(vector, dt)
        
        PIDSubject.send_output(output, error)

    except Exception as e:
        print(f"PID更新处理错误: {e}")