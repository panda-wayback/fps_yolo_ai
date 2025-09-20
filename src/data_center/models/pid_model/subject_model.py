"""
统一管理PID模型相关的话题
"""

from rx.subject import Subject



class PIDSubjectModel:
    """PID模型订阅统一接口"""
    config_subject = Subject()
    update_subject = Subject()
    output_subject = Subject()

