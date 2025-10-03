
# 使用 pynput 移动鼠标
from pynput.mouse import Controller
import time

if __name__ == "__main__":
    # 创建鼠标控制器
    mouse = Controller()
    
    # 获取当前鼠标位置
    current_pos = mouse.position
    print(f"当前鼠标位置: {current_pos}")
    
    # 相对移动鼠标 (dx, dy)
    print("移动鼠标 (100, 100)...")
    mouse.move(100, 100)
    
