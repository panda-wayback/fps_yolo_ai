#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一管理鼠标驱动模型相关的话题
基于PID模型的最佳实践
"""

from rx.subject import Subject


class MouseDriverSubjectModel:
    """鼠标驱动模型话题统一管理"""
    
    # 所有鼠标驱动相关的话题作为静态变量
    config_subject = Subject()      # 鼠标驱动配置话题
    vector_subject = Subject()      # 鼠标向量话题
