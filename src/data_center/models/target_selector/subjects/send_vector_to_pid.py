from typing import Tuple
from data_center.models.pid_model.subject import PIDSubject

def send_vector_to_pid(vector: Tuple[float, float]):
    """发送向量到PID"""
    PIDSubject.send_update(vector)