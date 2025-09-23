
import threading
from pynput import mouse
import time
from data_center.index import get_data_center


class InputMonitorState:
    """输入监控器状态"""
    @staticmethod
    def get_state():
        return get_data_center().state.input_monitor_state
    
    @staticmethod
    def monitor_mouse_click(x, y, button, pressed):
        print(f"鼠标点击: {button} {pressed}, 时间: {time.time()}")
        if pressed:
            if button == mouse.Button.left:
                InputMonitorState.get_state().mouse_left_click_time.set(time.time())
            elif button == mouse.Button.right:
                InputMonitorState.get_state().mouse_right_click_time.set(time.time())




def start_mouse_listener():
    with mouse.Listener(
        # on_move=on_move,
        on_click=InputMonitorState.monitor_mouse_click,
        # on_scroll=on_scroll
        ) as listener:
        listener.join()

# 启动鼠标监听器线程
listener_thread = threading.Thread(target=start_mouse_listener)
listener_thread.start()
