

from functions.get_pid_res import get_pid_res
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_default_mouse_simulator
from utils.move_mouse.move_mouse import move_mouse


def run_move_mouse(x_output, y_output):
    """
    运行鼠标移动
    """
    move_mouse(x_output, y_output)

def run_move_mouse_by_pid(results, image_size):
    """
    运行鼠标移动
    """
    x_output, y_output = get_pid_res(results, image_size)
    print(f"PID控制器输出: {x_output, y_output}")
    get_default_mouse_simulator().submit_vector(-x_output, -y_output)
    # move_mouse(-x_output, -y_output)
    