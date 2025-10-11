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
        
        self.mouse_listener_thread = None
        self.keyboard_listener_thread = None
        self.is_running = False
        self._initialized = True
        self.start()
    
    def start_mouse_listener(self):
        """启动鼠标监听器"""
        from data_center.models.input_monitor.subject import InputMonitorSubject
        with mouse.Listener(
            on_move=InputMonitorSubject.on_mouse_move,
            on_click=InputMonitorSubject.monitor_mouse_click,
        ) as listener:
            listener.join()
    
    def start_keyboard_listener(self):
        """启动键盘监听器"""
        from data_center.models.input_monitor.subject import InputMonitorSubject
        with keyboard.Listener(
            on_press=InputMonitorSubject.monitor_keyboard_press
        ) as listener:
            listener.join()
    
    def start(self):
        """启动输入监控"""
        if self.is_running:
            print("输入监控已经在运行中")
            return
        
        self.is_running = True
        
        # 启动鼠标监听器线程
        self.mouse_listener_thread = threading.Thread(target=self.start_mouse_listener, daemon=True)
        self.mouse_listener_thread.start()
        
        # 启动键盘监听器线程
        self.keyboard_listener_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        self.keyboard_listener_thread.start()
        
        print("✅ 输入监控已启动")
    
    def stop(self):
        """停止输入监控"""
        self.is_running = False
        self.mouse_listener_thread.join(timeout=1.0)
        self.keyboard_listener_thread.join(timeout=1.0)
        print("⏹️ 输入监控已停止")


def get_input_monitor() -> InputMonitor:
    """
    获取输入监控单例实例
    
    Returns:
        InputMonitor: 输入监控单例实例
    """
    return InputMonitor()


if __name__ == "__main__":
    input_monitor = get_input_monitor()
    time.sleep(10)