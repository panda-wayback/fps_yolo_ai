
import time
from pynput import mouse

from data_center.models.input_monitor.state import InputMonitorState
from data_center.models.screenshot.subject import ScreenshotSubject

class InputMonitorSubject:
        
    @staticmethod
    # 监听鼠标点击
    def monitor_mouse_click(x, y, button, pressed):
        # print(f"鼠标点击: {button} {pressed}, 时间: {time.time()}")
        if pressed:
            if button == mouse.Button.left:
                InputMonitorState.get_state().mouse_left_click_time.set(time.time())
            elif button == mouse.Button.right:
                InputMonitorState.get_state().mouse_right_click_time.set(time.time())
    
    # 监听键盘按键
    @staticmethod
    def monitor_keyboard_press(key):
        """监控键盘按键"""
        print(f"键盘按键: {key}")
        try:
            # 获取按键名称
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            InputMonitorState.get_state().keyboard_click_name.set(key_name)
        except AttributeError:
            # 处理特殊按键（如方向键、功能键等）
            key_name = str(key)
            InputMonitorState.get_state().keyboard_click_name.set(key_name)
    
    # 监听鼠标移动
    @staticmethod
    def on_mouse_move(x, y):
        print(f"鼠标移动: {x}, {y}")
        ScreenshotSubject.send_config(mouse_pos=(x, y))
        pass
