from typing import Tuple

from data_center.models.mouse_driver_model.subject import MouseDriverSubject


def send_mouse_driver(vector: Tuple[float, float]):
    """发送鼠标驱动"""
    MouseDriverSubject.send_vector(vector)
    pass