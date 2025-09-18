#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标跟踪器控制组件
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, 
                               QSlider, QDoubleSpinBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QShortcut, QKeySequence
from pyside.UI.basic.basic_layout import create_vertical_card
from singleton_classes.target_tracker.target_tracker import TargetTracker


def create_slider_control(title, min_val, max_val, default_val, decimals=2):
    """
    创建滑块控制组件
    
    Args:
        title: 参数名称
        min_val: 最小值
        max_val: 最大值  
        default_val: 默认值
        decimals: 小数位数
        
    Returns:
        QGroupBox: 滑块控制组件
    """
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


def create_target_tracker_control():
    """
    创建目标跟踪器控制组件
    
    Returns:
        QGroupBox: 目标跟踪器控制组件
    """
    # 创建主容器
    group = create_vertical_card("目标跟踪器控制")
    layout = group._layout
    
    # 获取目标跟踪器单例
    tracker = TargetTracker()
    
    # 状态监控区域（放在最上方）
    monitor_group = create_vertical_card("状态监控")
    monitor_layout = monitor_group._layout
    
    # 状态信息显示
    info_text = QLabel("等待启动...")
    info_text.setWordWrap(True)
    info_text.setStyleSheet("""
        QLabel {
            background-color: #f5f5f5; 
            color: #333333;
            padding: 10px; 
            border-radius: 5px;
            border: 1px solid #cccccc;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
        }
    """)
    monitor_layout.addWidget(info_text)
    
    # 刷新按钮
    refresh_btn = QPushButton("刷新状态")
    monitor_layout.addWidget(refresh_btn)
    
    layout.addWidget(monitor_group)
    
    # 控制按钮
    start_btn = QPushButton("启动跟踪 (F1)")
    stop_btn = QPushButton("停止跟踪 (F2)")
    reset_btn = QPushButton("重置 (F3)")
    
    # 按钮样式
    start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
    stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
    reset_btn.setStyleSheet("QPushButton { background-color: #ff9800; color: white; font-weight: bold; }")
    
    # 按钮布局
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(start_btn)
    btn_layout.addWidget(stop_btn)
    btn_layout.addWidget(reset_btn)
    layout.addLayout(btn_layout)
    
    # 参数控制区域
    params_group = create_vertical_card("跟踪参数")
    params_layout = params_group._layout
    
    # FPS控制
    fps_control = create_slider_control("跟踪频率", 10, 120, 60, 0)
    params_layout.addWidget(fps_control)
    
    # 应用参数按钮
    apply_btn = QPushButton("应用参数")
    apply_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
    params_layout.addWidget(apply_btn)
    
    layout.addWidget(params_group)
    
    # 定时器用于状态更新
    status_timer = QTimer()
    status_timer.timeout.connect(lambda: update_status_display())
    
    def update_status_display():
        """更新状态显示"""
        try:
            status = tracker.get_status()
            
            # 更新详细信息
            info = f"""
                跟踪状态: {'运行中' if status['running'] and status['thread_alive'] else '已停止'}
                跟踪频率: {status['fps']} FPS
                线程状态: {'活跃' if status['thread_alive'] else '已结束'}
                目标选择状态: {status['target_selector']}
                当前目标: {status['current_target']}
            """
            info_text.setText(info.strip())
        except Exception as e:
            info_text.setText(f"状态获取错误: {e}")
    
    # 按钮事件处理
    def on_start():
        """启动目标跟踪"""
        tracker.start()
        status_timer.start(100)  # 每100ms更新一次状态
        print("🎯 启动目标跟踪")
    
    def on_stop():
        """停止目标跟踪"""
        tracker.stop()
        print("🛑 停止目标跟踪")
    
    def on_reset():
        """重置目标跟踪"""
        tracker.stop()
        print("🔄 重置目标跟踪")
    
    def on_apply_params():
        """应用参数设置"""
        fps = int(fps_control.spinbox.value())
        tracker.set_fps(fps)
        print(f"✅ 应用参数: FPS={fps}")
    
    def on_refresh():
        """刷新状态"""
        update_status_display()
        print("🔄 刷新状态")
    
    # 连接按钮事件
    start_btn.clicked.connect(on_start)
    stop_btn.clicked.connect(on_stop)
    reset_btn.clicked.connect(on_reset)
    apply_btn.clicked.connect(on_apply_params)
    refresh_btn.clicked.connect(on_refresh)
    
    # 设置快捷键
    start_shortcut = QShortcut(QKeySequence(Qt.Key_F1), group)
    start_shortcut.activated.connect(on_start)
    
    stop_shortcut = QShortcut(QKeySequence(Qt.Key_F2), group)
    stop_shortcut.activated.connect(on_stop)
    
    reset_shortcut = QShortcut(QKeySequence(Qt.Key_F3), group)
    reset_shortcut.activated.connect(on_reset)
    
    # 存储引用到组件
    group.status_timer = status_timer
    group.tracker = tracker
    group.info_text = info_text
    group.start_shortcut = start_shortcut
    group.stop_shortcut = stop_shortcut
    group.reset_shortcut = reset_shortcut
    
    return group


def get_target_tracker_control():
    """
    获取目标跟踪器控制组件
    
    Returns:
        QGroupBox: 目标跟踪器控制组件
    """
    return create_target_tracker_control()
