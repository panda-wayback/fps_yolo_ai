# -*- coding: utf-8 -*-
"""
Windows鼠标控制器
使用Windows API直接控制鼠标，解决pynput无法控制Steam游戏的问题
基于ctypes调用Windows SendInput API实现鼠标控制
"""

import ctypes
import ctypes.wintypes
from typing import Tuple


class WindowsMouseController:
    """
    Windows鼠标控制器
    使用Windows API直接控制鼠标，可以控制Steam游戏中的鼠标
    """
    
    # Windows API常量
    INPUT_MOUSE = 0
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    MOUSEEVENTF_ABSOLUTE = 0x8000
    
    def __init__(self):
        """初始化Windows鼠标控制器"""
        # 设置DPI感知，确保坐标正确
        try:
            PROCESS_PER_MONITOR_DPI_AWARE = 2
            ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        except:
            pass  # 如果设置失败，继续执行
        
        # 获取屏幕尺寸
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        # 获取DPI缩放因子
        try:
            hdc = ctypes.windll.user32.GetDC(0)
            dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            dpi_y = ctypes.windll.gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
            ctypes.windll.user32.ReleaseDC(0, hdc)
            self.dpi_scale_x = dpi_x / 96.0
            self.dpi_scale_y = dpi_y / 96.0
        except:
            self.dpi_scale_x = 1.0
            self.dpi_scale_y = 1.0
        
        # 当前鼠标位置（用于相对移动）
        self._current_x = 0
        self._current_y = 0
        
        # 初始化时获取当前鼠标位置
        self._update_current_position()
    
    def _update_current_position(self):
        """更新当前鼠标位置"""
        point = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        self._current_x = point.x
        self._current_y = point.y
    
    @property
    def position(self) -> Tuple[int, int]:
        """
        获取当前鼠标位置
        
        Returns:
            Tuple[int, int]: (x, y) 坐标
        """
        self._update_current_position()
        return (self._current_x, self._current_y)
    
    def move(self, dx: int, dy: int):
        """
        相对移动鼠标
        
        Args:
            dx (int): X方向移动距离（像素）
            dy (int): Y方向移动距离（像素）
        """
        if dx == 0 and dy == 0:
            return
        
        # 应用DPI缩放
        scaled_dx = int(dx * self.dpi_scale_x)
        scaled_dy = int(dy * self.dpi_scale_y)
        
        # 创建鼠标输入结构
        class MouseInput(ctypes.Structure):
            _fields_ = [
                ('dx', ctypes.c_long),
                ('dy', ctypes.c_long),
                ('mouseData', ctypes.wintypes.DWORD),
                ('dwFlags', ctypes.wintypes.DWORD),
                ('time', ctypes.wintypes.DWORD),
                ('dwExtraInfo', ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        class InputUnion(ctypes.Union):
            _fields_ = [('mi', MouseInput)]
        
        class Input(ctypes.Structure):
            _fields_ = [
                ('type', ctypes.wintypes.DWORD),
                ('ii', InputUnion)
            ]
        
        # 创建鼠标移动事件
        mouse_input = MouseInput()
        mouse_input.dx = scaled_dx
        mouse_input.dy = scaled_dy
        mouse_input.mouseData = 0
        mouse_input.dwFlags = self.MOUSEEVENTF_MOVE
        mouse_input.time = 0
        mouse_input.dwExtraInfo = None
        
        # 创建输入结构
        input_struct = Input()
        input_struct.type = self.INPUT_MOUSE
        input_struct.ii.mi = mouse_input
        
        # 发送输入事件
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(Input))
        
        # 更新内部位置记录（使用原始值，不缩放）
        self._current_x += dx
        self._current_y += dy
    
    def click(self, button: str = 'left', count: int = 1):
        """
        点击鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
            count (int): 点击次数
        """
        for _ in range(count):
            if button == 'left':
                self._mouse_event(self.MOUSEEVENTF_LEFTDOWN)
                self._mouse_event(self.MOUSEEVENTF_LEFTUP)
            elif button == 'right':
                self._mouse_event(self.MOUSEEVENTF_RIGHTDOWN)
                self._mouse_event(self.MOUSEEVENTF_RIGHTUP)
            elif button == 'middle':
                self._mouse_event(self.MOUSEEVENTF_MIDDLEDOWN)
                self._mouse_event(self.MOUSEEVENTF_MIDDLEUP)
    
    def press(self, button: str = 'left'):
        """
        按下鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
        """
        if button == 'left':
            self._mouse_event(self.MOUSEEVENTF_LEFTDOWN)
        elif button == 'right':
            self._mouse_event(self.MOUSEEVENTF_RIGHTDOWN)
        elif button == 'middle':
            self._mouse_event(self.MOUSEEVENTF_MIDDLEDOWN)
    
    def release(self, button: str = 'left'):
        """
        释放鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
        """
        if button == 'left':
            self._mouse_event(self.MOUSEEVENTF_LEFTUP)
        elif button == 'right':
            self._mouse_event(self.MOUSEEVENTF_RIGHTUP)
        elif button == 'middle':
            self._mouse_event(self.MOUSEEVENTF_MIDDLEUP)
    
    def _mouse_event(self, flags: int):
        """
        发送鼠标事件
        
        Args:
            flags (int): 鼠标事件标志
        """
        ctypes.windll.user32.mouse_event(flags, 0, 0, 0, 0)
    
    def scroll(self, dx: int, dy: int):
        """
        滚动鼠标滚轮
        
        Args:
            dx (int): 水平滚动距离
            dy (int): 垂直滚动距离
        """
        if dy != 0:
            # 垂直滚动
            ctypes.windll.user32.mouse_event(0x0800, 0, 0, dy * 120, 0)
        if dx != 0:
            # 水平滚动
            ctypes.windll.user32.mouse_event(0x1000, 0, 0, dx * 120, 0)


# 创建全局实例，保持与pynput.mouse.Controller()相同的接口
def get_windows_mouse_controller():
    """
    获取Windows鼠标控制器实例
    
    Returns:
        WindowsMouseController: 鼠标控制器实例
    """
    return WindowsMouseController()


# 为了兼容性，提供一个别名
Controller = WindowsMouseController


if __name__ == "__main__":
    # 测试代码
    mouse = WindowsMouseController()
    
    print(f"当前鼠标位置: {mouse.position}")
    
    # 测试相对移动
    print("测试相对移动...")
    mouse.move(100, 100)
    print(f"移动后位置: {mouse.position}")
    
    # 测试点击
    print("测试左键点击...")
    mouse.click('left')
    
    print("测试完成！")
