import threading
from pynput import mouse
import time

# 初始化全局变量
last_move_time = 0
last_left_click_time = 0
last_right_click_time = 0
last_scroll_time = 0
last_left_release_time = 0
last_right_release_time = 0

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


# 获取上次状态时间的函数
def get_last_event_times():
    global last_left_click_time, last_right_click_time, last_left_release_time, last_right_release_time
    return int(last_left_click_time*1000),int(last_right_click_time*1000),int(last_left_release_time*1000),int(last_right_release_time*1000)


# 鼠标监听器线程
def start_mouse_listener():
    with mouse.Listener(
            # on_move=on_move,
            on_click=on_click,
            # on_scroll=on_scroll
            ) as listener:
        listener.join()

# 启动鼠标监听器线程
listener_thread = threading.Thread(target=start_mouse_listener)
listener_thread.start()