#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一管理截图模型相关的话题
基于PID模型的最佳实践
"""

from rx.subject import Subject, BehaviorSubject


class ScreenshotSubjectModel:
    """截图模型话题统一管理"""
    
    # 所有截图相关的话题作为静态变量
    config_subject = Subject()          # 截图配置话题
    img_subject = BehaviorSubject(None) # 截图图片话题（BehaviorSubject保存最新值）
