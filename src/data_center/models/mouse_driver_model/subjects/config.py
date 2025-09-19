import time
from rx.subject import Subject

from data_center.index import get_data_center
from data_center.models.mouse_driver_model.state import MouseDriverState


subject = Subject()
def get_state():
    return get_data_center().get_state().mouse_driver_state

def send_config_subject(
    config: MouseDriverState,
):
    subject.on_next(config)

def submit_config(config: MouseDriverState):
    # 执行鼠标模拟器 - 延迟导入避免循环导入
    from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
    get_mouse_simulator().run()

def update_mouse_driver_state(config: MouseDriverState):
    # 更新数据中心状态
    get_state().merge_state(config)

def init_send_config_subject():
    subject.subscribe(submit_config)
    subject.subscribe(update_mouse_driver_state)
    pass

init_send_config_subject()

if __name__ == "__main__":
    send_config_subject(MouseDriverState(fps=1000, smoothing=0.4, max_duration=0.05, decay_rate=0.95, running=True))
    print(get_state())
    time.sleep(1)