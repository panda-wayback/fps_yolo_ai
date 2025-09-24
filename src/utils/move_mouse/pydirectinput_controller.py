# -*- coding: utf-8 -*-
"""
PyDirectInput鼠标控制器
使用pydirectinput库控制鼠标，专门解决游戏兼容性问题
pydirectinput使用DirectInput API，比标准Windows API更适合游戏环境
"""

import pydirectinput
import time
from typing import Tuple


class PyDirectInputMouseController:
    """
    PyDirectInput鼠标控制器
    使用pydirectinput库控制鼠标，专门解决Steam游戏兼容性问题
    """
    
    def __init__(self):
        """初始化PyDirectInput鼠标控制器"""
        # 设置pydirectinput配置
        pydirectinput.FAILSAFE = False  # 禁用安全模式，避免意外停止
        pydirectinput.PAUSE = 0.01  # 设置操作间隔
        
        # 当前鼠标位置（用于相对移动）
        self._current_x = 0
        self._current_y = 0
        
        # 初始化时获取当前鼠标位置
        self._update_current_position()
    
    def _update_current_position(self):
        """更新当前鼠标位置"""
        try:
            pos = pydirectinput.position()
            self._current_x = pos[0]
            self._current_y = pos[1]
        except:
            # 如果获取位置失败，保持当前值
            pass
    
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
        
        try:
            # 使用pydirectinput的相对移动
            pydirectinput.moveRel(dx, dy)
            
            # 更新内部位置记录
            self._current_x += dx
            self._current_y += dy
            
        except Exception as e:
            print(f"⚠️ 鼠标移动失败: {e}")
    
    def move_to(self, x: int, y: int):
        """
        绝对移动鼠标到指定位置
        
        Args:
            x (int): X坐标
            y (int): Y坐标
        """
        try:
            pydirectinput.moveTo(x, y)
            self._current_x = x
            self._current_y = y
        except Exception as e:
            print(f"⚠️ 鼠标移动到指定位置失败: {e}")
    
    def click(self, button: str = 'left', count: int = 1):
        """
        点击鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
            count (int): 点击次数
        """
        try:
            if button == 'left':
                pydirectinput.click(button='left', clicks=count)
            elif button == 'right':
                pydirectinput.click(button='right', clicks=count)
            elif button == 'middle':
                pydirectinput.click(button='middle', clicks=count)
        except Exception as e:
            print(f"⚠️ 鼠标点击失败: {e}")
    
    def press(self, button: str = 'left'):
        """
        按下鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
        """
        try:
            if button == 'left':
                pydirectinput.mouseDown(button='left')
            elif button == 'right':
                pydirectinput.mouseDown(button='right')
            elif button == 'middle':
                pydirectinput.mouseDown(button='middle')
        except Exception as e:
            print(f"⚠️ 鼠标按下失败: {e}")
    
    def release(self, button: str = 'left'):
        """
        释放鼠标按钮
        
        Args:
            button (str): 按钮类型 ('left', 'right', 'middle')
        """
        try:
            if button == 'left':
                pydirectinput.mouseUp(button='left')
            elif button == 'right':
                pydirectinput.mouseUp(button='right')
            elif button == 'middle':
                pydirectinput.mouseUp(button='middle')
        except Exception as e:
            print(f"⚠️ 鼠标释放失败: {e}")
    
    def scroll(self, dx: int, dy: int):
        """
        滚动鼠标滚轮
        
        Args:
            dx (int): 水平滚动距离
            dy (int): 垂直滚动距离
        """
        try:
            if dy != 0:
                # 垂直滚动
                pydirectinput.scroll(dy)
            if dx != 0:
                # 水平滚动（如果支持）
                pydirectinput.hscroll(dx)
        except Exception as e:
            print(f"⚠️ 鼠标滚动失败: {e}")
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.1):
        """
        拖拽鼠标
        
        Args:
            start_x (int): 起始X坐标
            start_y (int): 起始Y坐标
            end_x (int): 结束X坐标
            end_y (int): 结束Y坐标
            duration (float): 拖拽持续时间（秒）
        """
        try:
            pydirectinput.drag(start_x, start_y, end_x, end_y, duration=duration)
            self._current_x = end_x
            self._current_y = end_y
        except Exception as e:
            print(f"⚠️ 鼠标拖拽失败: {e}")


# 创建全局实例，保持与pynput.mouse.Controller()相同的接口
def get_pydirectinput_mouse_controller():
    """
    获取PyDirectInput鼠标控制器实例
    
    Returns:
        PyDirectInputMouseController: 鼠标控制器实例
    """
    return PyDirectInputMouseController()


# 为了兼容性，提供一个别名
Controller = PyDirectInputMouseController


if __name__ == "__main__":
    # 测试代码
    mouse = PyDirectInputMouseController()
    
    print(f"当前鼠标位置: {mouse.position}")
    
    # 测试相对移动
    print("测试相对移动...")
    mouse.move(100, 100)
    print(f"移动后位置: {mouse.position}")
    
    # 测试点击
    print("测试左键点击...")
    mouse.click('left')
    
    print("测试完成！")
