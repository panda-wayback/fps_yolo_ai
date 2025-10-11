from typing import Tuple

from data_center.models.mouse_driver_model.subject import MouseDriverSubject


def send_mouse_driver(vector: Tuple[float, float]):
    """发送鼠标驱动"""
    try:
        MouseDriverSubject.send_vector(vector)
    except Exception as e:
        print(f"❌ 发送鼠标驱动失败: {e}")
    pass