#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图设置组件
设置截图区域和参数
"""

from PySide6.QtWidgets import (QSpinBox, QLabel, QHBoxLayout, 
                               QVBoxLayout, QPushButton, QGroupBox)
from pyside.UI.basic.basic_layout import create_vertical_card

from data_center.models.screenshot.subject import ScreenshotSubject
from data_center.models.screenshot.state import ScreenshotModelState
from data_center.models.screenshot.model import (
    ScreenshotModel, 
    DEFAULT_REGION_SIZE, 
    DEFAULT_FPS
)
from singleton_classes.screenshot_img.main import get_screenshot


def create_screenshot_config():
    """
    创建截图设置组件
    
    Returns:
        QGroupBox: 截图设置组件
    """
    # 创建主容器
    group = create_vertical_card("截图设置")
    layout = group._layout
    
    # 从状态实例读取当前值（或使用默认常量）
    try:
        state = ScreenshotModelState.get_state()
        default_width, default_height = state.region_size.get()
        default_fps = int(state.fps.get())
    except:
        # 如果状态未初始化，使用模型默认常量
        default_width, default_height = DEFAULT_REGION_SIZE
        default_fps = DEFAULT_FPS
    
    # 截图区域设置
    region_group = QGroupBox("截图区域")
    region_layout = QVBoxLayout(region_group)
    
    # 宽度
    width_layout = QHBoxLayout()
    width_layout.addWidget(QLabel("宽度:"))
    width_spinbox = QSpinBox()
    width_spinbox.setRange(50, 2000)
    width_spinbox.setValue(default_width)  # 从模型读取默认宽度
    width_layout.addWidget(width_spinbox)
    region_layout.addLayout(width_layout)
    
    # 高度
    height_layout = QHBoxLayout()
    height_layout.addWidget(QLabel("高度:"))
    height_spinbox = QSpinBox()
    height_spinbox.setRange(50, 2000)
    height_spinbox.setValue(default_height)  # 从模型读取默认高度
    height_layout.addWidget(height_spinbox)
    region_layout.addLayout(height_layout)
    
    # 截图帧率设置
    fps_group = QGroupBox("截图帧率")
    fps_layout = QVBoxLayout(fps_group)
    
    # FPS设置
    fps_time_layout = QHBoxLayout()
    fps_time_layout.addWidget(QLabel("FPS:"))
    fps_spinbox = QSpinBox()
    fps_spinbox.setRange(1, 1000)
    fps_spinbox.setValue(int(default_fps))  # 从模型读取默认FPS
    fps_time_layout.addWidget(fps_spinbox)
    fps_layout.addLayout(fps_time_layout)
    
    # 按钮区域
    button_layout = QHBoxLayout()
    
    # 重置按钮
    reset_btn = QPushButton("重置")
    
    # 应用设置按钮
    apply_btn = QPushButton("应用设置")
    
    button_layout.addWidget(reset_btn)
    button_layout.addWidget(apply_btn)
    
    
    # 重置功能（使用模型默认常量）
    def reset_to_defaults():
        """重置为默认值（使用 ScreenshotModel 定义的常量）"""
        width_spinbox.setValue(DEFAULT_REGION_SIZE[0])  # 默认宽度
        height_spinbox.setValue(DEFAULT_REGION_SIZE[1])  # 默认高度
        fps_spinbox.setValue(DEFAULT_FPS)                # 默认FPS
        print("✅ 已重置为默认值")
    
    # 应用设置功能
    def apply_settings():
        """应用截图设置"""
        try:
            region_size = (width_spinbox.value(), height_spinbox.value())
            fps = fps_spinbox.value()
            
            ScreenshotSubject.send_config(None, region_size, fps)
            get_screenshot().start()
            
            print(f"✅ 截图设置已应用: 区域={region_size}, FPS={fps}")
            
        except Exception as e:
            print(f"❌ 应用设置失败: {str(e)}")
    
    
    # 连接按钮事件
    reset_btn.clicked.connect(reset_to_defaults)
    apply_btn.clicked.connect(apply_settings)
    
    
    # 添加到布局
    layout.addWidget(region_group)
    layout.addWidget(fps_group)
    layout.addLayout(button_layout)
    
    return group


def get_screenshot_config():
    """
    获取截图设置组件
    
    Returns:
        QGroupBox: 截图设置组件
    """
    return create_screenshot_config()
