# -*- coding: utf-8 -*-
"""
Windows鼠标控制工具
使用ctypes调用Windows API实现鼠标相对移动功能
通过SendInput API直接向系统发送鼠标输入事件

@Time : 2022/10/24 10:22
@Author : cxk
@File : z_ctypes.py
@Software : PyCharm
"""

import ctypes

# Windows API数据类型定义
# 这些类型对应Windows API中的C语言数据类型
LONG = ctypes.c_long        # 32位有符号整数，对应Windows API中的LONG类型
DWORD = ctypes.c_ulong      # 32位无符号整数，对应Windows API中的DWORD类型
ULONG_PTR = ctypes.POINTER(DWORD)  # 指向DWORD的指针，用于存储额外信息
WORD = ctypes.c_ushort      # 16位无符号整数，对应Windows API中的WORD类型

# Windows API常量定义
INPUT_MOUSE = 0  # 输入类型：鼠标输入，对应Windows API中的INPUT_MOUSE常量


class MouseInput(ctypes.Structure):
    """
    鼠标输入结构体
    对应Windows API中的MOUSEINPUT结构体
    用于描述鼠标输入事件的详细信息
    """
    _fields_ = [
        ('dx', LONG),           # X方向移动距离（相对移动）
        ('dy', LONG),           # Y方向移动距离（相对移动）
        ('mouseData', DWORD),   # 鼠标数据（滚轮数据等）
        ('dwFlags', DWORD),     # 鼠标事件标志位（移动、点击、滚轮等）
        ('time', DWORD),        # 时间戳（通常设为0，让系统自动设置）
        ('dwExtraInfo', ULONG_PTR)  # 额外信息指针（通常设为None）
    ]


class InputUnion(ctypes.Union):
    """
    输入联合体
    对应Windows API中的INPUT_UNION结构体
    可以包含不同类型的输入（鼠标、键盘等）
    """
    _fields_ = [
        ('mi', MouseInput)  # 鼠标输入结构体
    ]


class Input(ctypes.Structure):
    """
    输入结构体
    对应Windows API中的INPUT结构体
    用于包装具体的输入事件
    """
    _fields_ = [
        ('types', DWORD),      # 输入类型（鼠标、键盘等）
        ('iu', InputUnion)     # 输入联合体，包含具体的输入数据
    ]


def mouse_input_set(flags, x, y, data):
    """
    创建鼠标输入结构体
    
    Args:
        flags (int): 鼠标事件标志位
                    MOUSEEVENTF_MOVE = 0x0001 (相对移动)
                    MOUSEEVENTF_LEFTDOWN = 0x0002 (左键按下)
                    MOUSEEVENTF_LEFTUP = 0x0004 (左键释放)
                    MOUSEEVENTF_RIGHTDOWN = 0x0008 (右键按下)
                    MOUSEEVENTF_RIGHTUP = 0x0010 (右键释放)
                    MOUSEEVENTF_WHEEL = 0x0800 (滚轮)
        x (int): X方向移动距离（相对移动时使用）
        y (int): Y方向移动距离（相对移动时使用）
        data (int): 鼠标数据（滚轮滚动量等）
    
    Returns:
        MouseInput: 鼠标输入结构体实例
    """
    return MouseInput(x, y, data, flags, 0, None)


def input_do(structure):
    """
    将输入结构体包装成INPUT结构体
    
    Args:
        structure: 输入结构体（MouseInput等）
    
    Returns:
        Input: 包装后的INPUT结构体
    
    Raises:
        TypeError: 当输入结构体类型不支持时抛出异常
    """
    if isinstance(structure, MouseInput):
        # 创建INPUT结构体，类型为鼠标输入，包含鼠标输入数据
        return Input(INPUT_MOUSE, InputUnion(mi=structure))
    raise TypeError('Cannot create Input structure!')


def mouse_input(flags, x=0, y=0, data=0):
    """
    创建鼠标输入事件
    
    Args:
        flags (int): 鼠标事件标志位
        x (int, optional): X方向移动距离，默认为0
        y (int, optional): Y方向移动距离，默认为0
        data (int, optional): 鼠标数据，默认为0
    
    Returns:
        Input: 包装好的鼠标输入事件
    
    Example:
        # 相对移动鼠标
        mouse_input(0x0001, 100, 50)  # 向右移动100像素，向下移动50像素
        
        # 左键点击
        mouse_input(0x0002)  # 左键按下
        mouse_input(0x0004)  # 左键释放
        
        # 滚轮滚动
        mouse_input(0x0800, data=120)  # 向上滚动
    """
    return input_do(mouse_input_set(flags, x, y, data))


def SendInput(*inputs):
    """
    向系统发送输入事件
    调用Windows API的SendInput函数
    
    Args:
        *inputs: 可变参数，可以传入多个Input结构体
    
    Returns:
        int: 成功发送的输入事件数量
        
    Note:
        这是Windows API的核心函数，直接向系统发送输入事件
        比pynput等库更底层，性能更好，但只支持Windows系统
    """
    n_inputs = len(inputs)  # 输入事件的数量
    lp_input = Input * n_inputs  # 创建Input结构体数组类型
    p_inputs = lp_input(*inputs)  # 创建Input结构体数组实例
    cb_size = ctypes.c_int(ctypes.sizeof(Input))  # Input结构体的大小
    
    # 调用Windows API的SendInput函数
    # 参数：输入数量，输入数组，结构体大小
    return ctypes.windll.user32.SendInput(n_inputs, p_inputs, cb_size)


if __name__ == '__main__':
    # 测试代码：相对移动鼠标
    # 参数说明：
    # 1: MOUSEEVENTF_MOVE标志位，表示相对移动
    # -100: 向左移动100像素
    # -200: 向上移动200像素
    SendInput(mouse_input(1, -100, -200))


