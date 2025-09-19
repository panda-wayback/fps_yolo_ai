from rx.subject import Subject

from data_center.index import get_data_center
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


subject = Subject()

# 发布向量
def send_vector_subject(vx, vy):
    subject.on_next((vx, vy))

# 执行鼠标模拟器提交向量
def submit_vector(vector: tuple[float, float]):
    # 执行鼠标模拟器提交向量
    get_mouse_simulator().submit_vector(vector)

def update_data_center_vector(vector: tuple[float, float]):
    get_data_center().get_state().mouse_driver_state.vx = vector[0]
    get_data_center().get_state().mouse_driver_state.vy = vector[1]
    
def init_send_vector_subject():
    subject.subscribe(lambda x: submit_vector(x))
    pass

init_send_vector_subject()

if __name__ == "__main__":
    send_vector_subject(1, 1)




