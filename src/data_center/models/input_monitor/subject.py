
import threading
from pynput import mouse
from pynput import mouse, keyboard

import time
from data_center.models.input_monitor.state import InputMonitorState


class InputMonitorSubject:
        
    @staticmethod
    def monitor_mouse_click(x, y, button, pressed):
        # print(f"鼠标点击: {button} {pressed}, 时间: {time.time()}")
        if pressed:
            if button == mouse.Button.left:
                InputMonitorState.get_state().mouse_left_click_time.set(time.time())
            elif button == mouse.Button.right:
                InputMonitorState.get_state().mouse_right_click_time.set(time.time())
    
    @staticmethod
    def monitor_keyboard_press(key):
        """监控键盘按键"""
        try:
            # 获取按键名称
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            InputMonitorState.get_state().keyboard_click_name.set(key_name)
        except AttributeError:
            # 处理特殊按键（如方向键、功能键等）
            key_name = str(key)
            InputMonitorState.get_state().keyboard_click_name.set(key_name)


def start_mouse_listener():
    with mouse.Listener(
        # on_move=on_move,
        on_click=InputMonitorSubject.monitor_mouse_click,
        # on_scroll=on_scroll
        ) as listener:
        listener.join()

def start_keyboard_listener():
    with keyboard.Listener(
        on_press=InputMonitorSubject.monitor_keyboard_press
        ) as listener:
        listener.join()

# 启动鼠标监听器线程
mouse_listener_thread = threading.Thread(target=start_mouse_listener)
mouse_listener_thread.start()

# 启动键盘监听器线程
keyboard_listener_thread = threading.Thread(target=start_keyboard_listener)
keyboard_listener_thread.start()
