import numpy as np
from filterpy.kalman import KalmanFilter
import time

def make_kf(dt=1/120.0, q_pos=1.0, q_vel=10.0, r_meas=4.0, history_time=0.5):
    """
    创建卡尔曼滤波器，支持历史时间限制
    
    Args:
        dt: 时间步长
        q_pos: 位置过程噪声
        q_vel: 速度过程噪声
        r_meas: 测量噪声
        history_time: 保留历史的时间（秒），超过此时间会重置
    """
    kf = KalmanFilter(dim_x=4, dim_z=2, dim_u=2)
    kf.F = np.array([[1,0,dt,0],
                     [0,1,0,dt],
                     [0,0,1, 0],
                     [0,0,0, 1]], float)
    kf.H = np.array([[1,0,0,0],
                     [0,1,0,0]], float)
    # B: 控制量 u (你的屏幕移动速度) 对相对位置有相反影响
    kf.B = np.array([[-dt,   0],
                     [  0, -dt],
                     [  0,   0],
                     [  0,   0]], float)
    kf.x = np.array([0.,0.,0.,0.])
    kf.P *= 50.0
    kf.Q = np.diag([q_pos, q_pos, q_vel, q_vel])
    kf.R = np.diag([r_meas, r_meas])
    
    # 添加历史时间限制
    kf.history_time = history_time
    kf.start_time = time.time()
    
    return kf

# 使用示例（每帧调用）
kf = make_kf(dt=1/120.0, history_time=0.5)  # 只保留0.5秒历史

def frame_step(mouse_delta_pixels, detection, dt=1/120.0, lead_time=0.2):
    """
    每帧调用卡尔曼滤波，自动清除超过0.5秒的历史
    
    Args:
        mouse_delta_pixels: 鼠标/视角导致的屏幕平移（像素）
        detection: 目标相对中心偏移（像素），None表示丢失
        dt: 帧间时间（秒）
        lead_time: 预测时间（秒）
    
    Returns:
        tuple: (predicted_point, p, v)
    """
    # 检查是否需要重置（超过历史时间）
    current_time = time.time()
    if current_time - kf.start_time > kf.history_time:
        # 重置滤波器，清除历史
        kf.x = np.array([0.,0.,0.,0.])
        kf.P *= 50.0
        kf.start_time = current_time
        print("历史超过0.5秒，重置滤波器")
    
    # 将 mouse delta 换算成 像素/秒
    u = np.array(mouse_delta_pixels) / max(dt, 1e-6)
    kf.F[0,2] = kf.F[1,3] = dt  # 确保 F 与 dt 一致
    kf.B = np.array([[-dt,0],[0,-dt],[0,0],[0,0]])
    
    # 预测（带控制量）
    kf.predict(u=u)
    
    # 更新（若有检测）
    if detection is not None:
        kf.update(np.asarray(detection, dtype=float))
    
    # 前瞻输出
    p = kf.x[0:2]
    v = kf.x[2:4]
    predicted_point = p + v * lead_time
    
    return predicted_point, p, v

# 返回值： predicted_point（前瞻位置），p（当前估计相对位置），v（估计速度）
