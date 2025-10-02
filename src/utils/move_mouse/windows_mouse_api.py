import ctypes
from ctypes import wintypes, Structure, Union
import win32api
import win32con
import sys


def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """请求以管理员权限重新运行当前脚本"""
    if not is_admin():
        print("⚠️ 当前没有管理员权限，正在请求提升权限...")
        # 重新以管理员权限运行
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )

# ==================== 鼠标相对移动 ====================
def relative_move(dx, dy):
    """
    使用 win32api.mouse_event 进行相对移动
    
    这是最底层的 Windows API，游戏兼容性最好
    需要管理员权限才能控制游戏
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)


def get_cursor_pos():
    """获取当前鼠标位置"""
    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]
    
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return (point.x, point.y)
