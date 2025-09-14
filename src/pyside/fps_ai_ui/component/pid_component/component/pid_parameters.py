#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁的PID参数滑块组件
"""

from PySide6.QtWidgets import (QGroupBox, QHBoxLayout, QSlider, 
                               QDoubleSpinBox, QPushButton, QVBoxLayout)
from PySide6.QtCore import Qt
from functions.get_pid_res import get_pid_parameters, set_pid_parameters
from pyside.UI.basic.basic_layout import create_vertical_card


def create_slider_control(title, min_val, max_val, default_val, decimals=2) -> QGroupBox:
    """
    创建单个滑块控制组件
    
    Args:
        title: 参数名称
        min_val: 最小值
        max_val: 最大值  
        default_val: 默认值
        decimals: 小数位数
        
    Returns:
        QGroupBox: 滑块控制组件
    """
    # 使用 create_vertical_card 创建卡片
    group = create_vertical_card(title)
    layout = group._layout
    
    # 滑块
    slider = QSlider(Qt.Horizontal)
    slider.setRange(int(min_val * 100), int(max_val * 100))
    slider.setValue(int(default_val * 100))
    
    # 数值框
    spinbox = QDoubleSpinBox()
    spinbox.setRange(min_val, max_val)
    spinbox.setValue(default_val)
    spinbox.setDecimals(decimals)
    spinbox.setSingleStep(0.01)
    
    # 双向同步
    def on_slider_changed(value):
        spinbox.setValue(value / 100.0)
    
    def on_spinbox_changed(value):
        slider.setValue(int(value * 100))
    
    slider.valueChanged.connect(on_slider_changed)
    spinbox.valueChanged.connect(on_spinbox_changed)
    
    # 布局
    control_layout = QHBoxLayout()
    control_layout.addWidget(slider)
    control_layout.addWidget(spinbox)
    
    layout.addLayout(control_layout)
    
    # 存储引用
    group.slider = slider
    group.spinbox = spinbox
    
    return group


def get_pid_control_widget():
    """
    创建PID参数控制组件
    
    Returns:
        QGroupBox: PID控制组件
    """
    # 使用 create_vertical_card 创建主容器
    group = create_vertical_card("PID参数控制")
    layout: QVBoxLayout = group._layout

    # 获取PID参数5
    kp, ki, kd = get_pid_parameters()
    
    # 创建三个参数控制
    kp_control: QGroupBox = create_slider_control("Kp", 0, 50, kp, 2)
    ki_control: QGroupBox = create_slider_control("Ki", 0, 5, ki, 3)  
    kd_control: QGroupBox = create_slider_control("Kd", 0, 2, kd, 3)
    
    # 按钮
    apply_btn = QPushButton("应用")
    reset_btn = QPushButton("重置")
    load_btn = QPushButton("加载")
    
    # 按钮事件
    def apply_params():
        kp = kp_control.spinbox.value()
        ki = ki_control.spinbox.value()
        kd = kd_control.spinbox.value()
        set_pid_parameters(kp, ki, kd)
        print(f"应用PID参数: Kp={kp}, Ki={ki}, Kd={kd}")
    
    def reset_params():
        kp_control.spinbox.setValue(kp)
        ki_control.spinbox.setValue(ki)
        kd_control.spinbox.setValue(kd)
    
    def load_params():
        kp, ki, kd = get_pid_parameters()
        kp_control.spinbox.setValue(kp)
        ki_control.spinbox.setValue(ki)
        kd_control.spinbox.setValue(kd)
    
    apply_btn.clicked.connect(apply_params)
    reset_btn.clicked.connect(reset_params)
    load_btn.clicked.connect(load_params)
    
    # 按钮布局
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(apply_btn)
    btn_layout.addWidget(reset_btn)
    btn_layout.addWidget(load_btn)
    
    # 添加到主布局
    layout.addWidget(kp_control)
    layout.addWidget(ki_control)
    layout.addWidget(kd_control)
    layout.addLayout(btn_layout)
    
    return group