


from functions.get_target_vector import get_center_to_target_vector
from utils.pid.pid import PIDControl


# 调整 PID 参数，使其更适合瞄准控制
pid_control = PIDControl()

# 获取pid参数

def get_pid_parameters():
    """
    获取pid参数
    """
    return pid_control.get_pid_parameters()

# 设置pid参数
def set_pid_parameters(kp, ki, kd):
    """
    设置pid参数
    """
    pid_control.set_pid_parameters(kp, ki, kd)



def get_pid_res(results, image_size, dt = 0.02):
    """
    获取 PID 控制器输出
    
    Args:
        results: YOLO 检测结果
        image_size: 图像尺寸 (width, height)
        dt: 时间步长
    
    Returns:
        tuple: (x_output, y_output) 或 (0, 0) 如果没有目标
    """
    # 获取目标向量
    vector_result = get_center_to_target_vector(results, image_size)
    print(f"目标向量: {vector_result}")
    
    if vector_result is None:
        # 没有检测到目标，返回零输出
        return (0, 0)
    
    # 解包向量
    error_x, error_y = vector_result
    
    # # 添加调试信息
    # print(f"调试信息:")
    # print(f"  目标向量: ({error_x:.2f}, {error_y:.2f})")
    # print(f"  图像尺寸: {image_size}")
    # print(f"  时间步长: {dt}")
    
    # 使用 PID 控制器计算输出
    x_output, y_output = pid_control.update(error_x, error_y, dt)
    
    print(f"  PID输出: ({x_output:.2f}, {y_output:.2f})")
    
    return x_output, y_output