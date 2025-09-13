
# -*- coding: utf-8 -*-
"""
鼠标控制工具
使用pynput库实现简单的鼠标相对移动功能
"""

import time
from pynput.mouse import Controller

# 创建鼠标控制器实例
# Controller是pynput库提供的鼠标控制类，可以执行各种鼠标操作
mouse = Controller()

def move_mouse(x, y):
    """
    相对移动鼠标到指定位置
    
    Args:
        x (int): X方向移动距离（像素）
                正数向右移动，负数向左移动
        y (int): Y方向移动距离（像素）
                正数向下移动，负数向上移动
    
    Example:
        move_mouse(100, 50)   # 向右移动100像素，向下移动50像素
        move_mouse(-50, -30)  # 向左移动50像素，向上移动30像素
        move_mouse(0, 100)    # 只向下移动100像素
    """
    # 调用pynput的move方法进行相对移动
    # move方法接受两个参数：x和y的偏移量
    mouse.move(x, y)


# 获取鼠标当前位置
def get_mouse_position():
    return mouse.position

def test():
    while True:
        print(get_mouse_position())
        time.sleep(1)

if __name__ == "__main__":
    # 测试代码：向右移动100像素，向下移动50像素
    # 注意：这里duration参数在pynput的move方法中不存在，需要移除
    # move_mouse(100, 50)
    test()
    pass 