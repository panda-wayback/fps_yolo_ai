import time
from utils.move_mouse.windows_mouse_api import relative_move


class WindowsMouseController:
    """
    Windows 鼠标控制器
    
    使用 win32api.mouse_event 进行鼠标相对移动
    需要管理员权限才能控制游戏
    """
    
    def __init__(self):
        pass
    
    def move(self, dx: int, dy: int):
        """相对移动鼠标"""
        relative_move(dx, dy)

if __name__ == "__main__":
    from utils.move_mouse.windows_mouse_api import is_admin, run_as_admin
    
    print("="*60)
    print("鼠标移动测试 (win32api.mouse_event)")
    print("="*60)
    
    # 检查管理员权限
    if is_admin():
        print("✅ 以管理员权限运行")
    else:
        print("⚠️ 当前没有管理员权限")
        print("⚠️ 控制游戏需要管理员权限！")
        choice = input("\n是否以管理员权限重新运行? (y/n): ")
        if choice.lower() == 'y':
            run_as_admin()
            exit()
        else:
            print("继续以普通权限运行（可能无法控制游戏）...")
    
    print("\n3秒后开始移动，持续5秒")
    
    controller = WindowsMouseController()
    
    print("等待3秒...")
    time.sleep(3)
    
    print("开始移动！")
    start_time = time.time()
    while time.time() - start_time < 5:
        controller.move(1, 1)  # 每次移动1像素
        time.sleep(0.01)  # 100Hz
    
    print("✅ 测试完成！")