from pynput import mouse, keyboard
import time

# 初始化全局变量
last_move_time = 0
last_left_click_time = 0
last_right_click_time = 0
last_scroll_time = 0
last_left_release_time = 0
last_right_release_time = 0

# 监听器对象
mouse_listener = None
keyboard_listener = None

def on_move(x, y):
    global last_move_time
    last_move_time = time.time()
    print(f"Mouse moved to ({x}, {y}) at {last_move_time}")

def on_scroll(x, y, dx, dy):
    global last_scroll_time
    last_scroll_time = time.time()
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy}) at {last_scroll_time}")

def on_click(x, y, button, pressed):
    global last_left_click_time, last_right_click_time, last_left_release_time, last_right_release_time
    if pressed:
        if button == mouse.Button.left:
            last_left_click_time = time.time()
            print(f"Left button clicked at ({x}, {y}) at {last_left_click_time}")
        elif button == mouse.Button.right:
            last_right_click_time = time.time()
            print(f"Right button clicked at ({x}, {y}) at {last_right_click_time}")
    else:
        if button == mouse.Button.left:
            last_left_release_time = time.time()
            print(f"Left button released at ({x}, {y}) at {last_left_release_time}")
        elif button == mouse.Button.right:
            last_right_release_time = time.time()
            print(f"Right button released at ({x}, {y}) at {last_right_release_time}")

def on_press(key):
    print(f"键盘按键: {key}")
    # 按 ESC 键停止监听
    if str(key) == 'Key.esc':
        stop_listeners()

    # 按 o 启动
    if str(key) == 'Key.o':
        start_listeners()

def start_listeners():
    """启动监听器"""
    global mouse_listener, keyboard_listener
    
    # 启动鼠标监听器
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()
    
    # 启动键盘监听器
    keyboard_listener = keyboard.Listener(
        on_press=on_press
    )
    keyboard_listener.start()
    
    print("✅ 监听器已启动，按 ESC 键停止")

def stop_listeners():
    """停止监听器"""
    global mouse_listener, keyboard_listener
    
    if mouse_listener:
        mouse_listener.stop()
        print("⏹️ 鼠标监听器已停止")
    
    if keyboard_listener:
        keyboard_listener.stop()
        print("⏹️ 键盘监听器已停止")

def get_last_event_times():
    global last_left_click_time, last_right_click_time, last_left_release_time, last_right_release_time
    return int(last_left_click_time*1000), int(last_right_click_time*1000), int(last_left_release_time*1000), int(last_right_release_time*1000)


if __name__ == "__main__":
    # 启动监听器
    start_listeners()
    
    # # 等待键盘监听器结束（按ESC键）
    # if keyboard_listener:
    #     keyboard_listener.join()
    time.sleep(1000)