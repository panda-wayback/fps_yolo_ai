#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一管理YOLO模型相关的话题
基于PID模型的最佳实践
"""

from rx.subject import Subject


class YoloSubjectModel:
    """YOLO模型话题统一管理"""
    
    # 所有YOLO相关的话题作为静态变量
    result_subject = Subject()           # YOLO检测结果话题
    detect_subject = Subject()           # YOLO检测话题
    load_model_subject = Subject()       # YOLO模型加载话题
    selected_class_subject = Subject()   # YOLO选中类别话题
