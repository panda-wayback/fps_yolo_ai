#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一管理目标选择器相关的话题
基于PID模型的最佳实践
"""

from rx.subject import Subject


class TargetSelectorSubjectModel:
    """目标选择器话题统一管理"""
    
    # 所有目标选择器相关的话题作为静态变量
    config_subject = Subject()      # 目标选择器配置话题
    select_subject = Subject()      # 目标选择话题
