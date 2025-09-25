




import time
from sympy import threaded
from data_center.models.input_monitor.state import InputMonitorState


def listen_keyboard_to_start_screenshot(value):
    print(f"键盘按键: {value}")
    from singleton_classes.screenshot_img.main import get_screenshot
    from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
    if value == "o":
        get_screenshot().start()
        get_mouse_simulator().run()
        pass 
    elif value == "p":
        get_screenshot().stop()
        get_mouse_simulator().stop()
        pass
    pass


def listen_left_mouse_click(value):
    InputMonitorState.get_state().is_submit_vector.set(True)
    def set_submit_vector_false():
        time.sleep(InputMonitorState.get_state().mouse_left_click_submit_time.get())
        InputMonitorState.get_state().is_submit_vector.set(False)
    threaded(set_submit_vector_false)
    pass





