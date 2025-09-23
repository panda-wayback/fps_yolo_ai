import threading
from pynput import mouse
import time
from data_center.models.input_monitor.state import InputMonitorState

def monitor_mouse_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            InputMonitorState.get_state().mouse_left_click_time.set(time.time())
        elif button == mouse.Button.right:
            InputMonitorState.get_state().mouse_right_click_time.set(time.time())
    # else:
    #     if button == mouse.Button.left:
    #         last_left_release_time = time.time()
    #         print(f"Left button released at ({x}, {y}) at {last_left_release_time}")
    #     elif button == mouse.Button.right:
    #         last_right_release_time = time.time()
    #         print(f"Right button released at ({x}, {y}) at {last_right_release_time}")