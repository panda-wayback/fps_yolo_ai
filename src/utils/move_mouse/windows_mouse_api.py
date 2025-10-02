import ctypes
from ctypes import wintypes, Structure, Union

# 定义结构体
class MOUSEINPUT(Structure):
    _fields_ = [
        ("dx", wintypes.LONG),        # 相对移动X
        ("dy", wintypes.LONG),        # 相对移动Y  
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),  # 事件标志
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(Structure):
    class _INPUT(Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_input", _INPUT)
    ]

# 常量
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

def relative_move_sendinput(dx, dy):
    """使用 SendInput 进行相对移动（推荐）"""
    mouse_input = MOUSEINPUT()
    mouse_input.dx = dx
    mouse_input.dy = dy
    mouse_input.dwFlags = MOUSEEVENTF_MOVE
    
    input_struct = INPUT()
    input_struct.type = INPUT_MOUSE
    input_struct._input.mi = mouse_input
    
    # 发送输入
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))


def get_cursor_pos():
    """获取当前鼠标位置"""
    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]
    
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return (point.x, point.y)

if __name__ == '__main__':
    mouse_pos = get_cursor_pos()
    print(mouse_pos)



# 在需要的地方调用
# mouse_pos = get_cursor_pos()
# # 持续移动5秒，每次移动1个像素
# import time

# time.sleep(5)
# start_time = time.time()
# while time.time() - start_time < 5:
#     relative_move_sendinput(1, 0)  # 每次向右移动1个像素
#     time.sleep(0.01)  # 控制移动速度，1ms一次（可根据需要调整）