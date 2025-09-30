import threading
import time
from pynput import mouse, keyboard

class InputMonitor:
    """输入监控单例类"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        from data_center.models.input_monitor.subject import InputMonitorSubject
        
        # 创建并启动监听器（一次性）
        self.mouse_listener = mouse.Listener(
            on_move=InputMonitorSubject.on_mouse_move,
            on_click=InputMonitorSubject.monitor_mouse_click,
        )
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(
            on_press=InputMonitorSubject.monitor_keyboard_press
        )
        self.keyboard_listener.start()
        
        self._initialized = True
        print("✅ 输入监控已启动")


def get_input_monitor() -> InputMonitor:
    """
    获取输入监控单例实例
    
    Returns:
        InputMonitor: 输入监控单例实例
    """
    return InputMonitor()

if __name__ == "__main__":
    # input_monitor = get_input_monitor()
    # pass
    time.sleep(1000)