import time
import threading
import ctypes
from typing import Dict
from utils.singleton.main import singleton
from utils.move_mouse.windows_mouse_api import get_cursor_pos


@singleton
class InputMonitor:
    """
    输入监控单例类 - 纯 Windows 原生实现
    
    鼠标移动：Windows API GetCursorPos 轮询
    鼠标点击：Windows API GetAsyncKeyState 轮询
    键盘：Windows API GetAsyncKeyState 轮询
    
    完全不依赖第三方库，100% 游戏兼容
    """
    
    def __init__(self, poll_rate: int = 120, monitor_keys: list = None):
        """
        初始化输入监控
        
        Args:
            poll_rate: 轮询频率（Hz），默认 120Hz
            monitor_keys: 要监控的按键列表（虚拟键码），None 表示监控常用按键
        """
        from data_center.models.input_monitor.subject import InputMonitorSubject
        
        self.poll_rate = poll_rate
        self._running = True
        self._last_pos = (0, 0)
        self._last_left_state = False
        self._last_right_state = False
        
        # Windows 虚拟键码 - 鼠标
        self.VK_LBUTTON = 0x01  # 左键
        self.VK_RBUTTON = 0x02  # 右键
        
        # 设置要监控的键盘按键（如果未指定，使用常用按键）
        if monitor_keys is None:
            # 默认监控常用游戏按键
            self.monitor_keys = {
                # 字母键 A-Z
                **{chr(i): i for i in range(0x41, 0x5B)},  # A-Z (0x41-0x5A)
                # 数字键 0-9
                **{str(i): 0x30 + i for i in range(10)},
                # 功能键
                'space': 0x20, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
                'esc': 0x1B, 'tab': 0x09, 'enter': 0x0D, 'backspace': 0x08,
                # 方向键
                'left': 0x25, 'up': 0x26, 'right': 0x27, 'down': 0x28,
                # F1-F12
                **{f'f{i}': 0x70 + i - 1 for i in range(1, 13)},
            }
        else:
            self.monitor_keys = monitor_keys
        
        # 记录按键状态（避免重复触发）
        self._key_states: Dict[int, bool] = {vk: False for vk in self.monitor_keys.values()}
        
        # 启动统一轮询线程（鼠标 + 键盘）
        self._poll_thread = threading.Thread(target=self._poll_inputs, daemon=True)
        self._poll_thread.start()
        
        print(f"✅ 输入监控已启动（Windows 原生 API，轮询: {poll_rate}Hz，监控 {len(self.monitor_keys)} 个按键）")
    
    def _check_key_state(self, vk_code):
        """检查按键状态（Windows API）"""
        # GetAsyncKeyState 返回值：最高位为1表示按下
        state = ctypes.windll.user32.GetAsyncKeyState(vk_code)
        return (state & 0x8000) != 0
    
    def _get_key_name_from_vk(self, vk_code):
        """根据虚拟键码获取键名"""
        for name, code in self.monitor_keys.items():
            if code == vk_code:
                return name
        return f'vk_{vk_code}'
    
    def _poll_inputs(self):
        """统一轮询鼠标和键盘（Windows API）"""
        from data_center.models.input_monitor.subject import InputMonitorSubject
        
        # 创建模拟鼠标按钮对象
        class MouseButton:
            left = "left"
            right = "right"
        
        # 创建键盘事件对象
        class KeyboardEvent:
            def __init__(self, name):
                self.name = name
                # 如果是单字符，设置 char 属性
                self.char = name if len(name) == 1 else None
            
            def __str__(self):
                return self.name
        
        interval = 1.0 / self.poll_rate
        
        while self._running:
            try:
                # ===== 1. 检查鼠标位置 =====
                current_pos = get_cursor_pos()
                if current_pos != self._last_pos:
                    InputMonitorSubject.on_mouse_move(current_pos[0], current_pos[1])
                    self._last_pos = current_pos
                
                # ===== 2. 检查鼠标左键状态 =====
                left_pressed = self._check_key_state(self.VK_LBUTTON)
                if left_pressed != self._last_left_state:
                    InputMonitorSubject.monitor_mouse_click(
                        current_pos[0], current_pos[1], 
                        MouseButton.left, 
                        left_pressed
                    )
                    self._last_left_state = left_pressed
                
                # ===== 3. 检查鼠标右键状态 =====
                right_pressed = self._check_key_state(self.VK_RBUTTON)
                if right_pressed != self._last_right_state:
                    InputMonitorSubject.monitor_mouse_click(
                        current_pos[0], current_pos[1], 
                        MouseButton.right, 
                        right_pressed
                    )
                    self._last_right_state = right_pressed
                
                # ===== 4. 检查键盘按键状态 =====
                for vk_code, last_state in list(self._key_states.items()):
                    current_state = self._check_key_state(vk_code)
                    
                    # 只在状态变化且为按下时触发
                    if current_state != last_state and current_state:
                        key_name = self._get_key_name_from_vk(vk_code)
                        key_event = KeyboardEvent(key_name)
                        InputMonitorSubject.monitor_keyboard_press(key_event)
                    
                    # 更新状态
                    self._key_states[vk_code] = current_state
                
                time.sleep(interval)
            except Exception as e:
                print(f"❌ 输入监控错误: {e}")
                time.sleep(0.1)
    
    def stop(self):
        """停止监控"""
        self._running = False
        print("⏹ 输入监控已停止")


def get_input_monitor() -> InputMonitor:
    """
    获取输入监控单例实例
    
    Returns:
        InputMonitor: 输入监控单例实例
    """
    return InputMonitor()

if __name__ == "__main__":
    input_monitor = get_input_monitor()
    from data_center.models.input_monitor.state import InputMonitorState
    InputMonitorState.init_subscribes()
    # pass
    time.sleep(1000)