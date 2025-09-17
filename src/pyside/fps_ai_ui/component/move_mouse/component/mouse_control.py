#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标模拟器控制组件
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, 
                               QLabel, QSlider, QDoubleSpinBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QShortcut, QKeySequence
from pyside.UI.basic.basic_layout import create_vertical_card
from singleton_classes.simulation_move_mouse.simulation_move_mouse import MouseSimulator


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


def create_mouse_control():
    """
    创建鼠标模拟器控制组件
    
    Returns:
        QGroupBox: 鼠标控制组件
    """
    # 创建主容器
    group = create_vertical_card("鼠标模拟器控制")
    layout = group._layout
    
    # 获取鼠标模拟器单例
    mouse_sim = MouseSimulator()
    
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
    start_btn = QPushButton("启动 (F4)")
    stop_btn = QPushButton("停止 (F5)")
    reset_btn = QPushButton("重置 (F6)")
    
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
    params_group = create_vertical_card("参数设置")
    params_layout = params_group._layout
    
    # FPS控制
    fps_control = create_slider_control("FPS", 100, 1000, 500, 0)
    params_layout.addWidget(fps_control)
    
    # 平滑系数控制
    smoothing_control = create_slider_control("平滑系数", 0.1, 1.0, 0.4, 2)
    params_layout.addWidget(smoothing_control)
    
    # 减速系数控制
    decay_control = create_slider_control("减速系数", 0.8, 0.99, 0.95, 3)
    params_layout.addWidget(decay_control)
    
    # 最大持续时间控制
    duration_control = create_slider_control("最大持续时间(秒)", 0.01, 0.2, 0.05, 3)
    params_layout.addWidget(duration_control)
    
    # 应用参数按钮
    apply_btn = QPushButton("应用参数")
    apply_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
    params_layout.addWidget(apply_btn)
    
    layout.addWidget(params_group)
    
    # 速度控制区域
    speed_group = create_vertical_card("速度控制")
    speed_layout = speed_group._layout
    
    # X轴速度
    vx_label = QLabel("X轴速度 (像素/秒):")
    vx_input = QDoubleSpinBox()
    vx_input.setRange(-1000, 1000)
    vx_input.setValue(0)
    vx_input.setSuffix(" px/s")
    
    # Y轴速度
    vy_label = QLabel("Y轴速度 (像素/秒):")
    vy_input = QDoubleSpinBox()
    vy_input.setRange(-1000, 1000)
    vy_input.setValue(0)
    vy_input.setSuffix(" px/s")
    
    # 提交速度按钮
    submit_btn = QPushButton("提交速度")
    submit_btn.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; }")
    
    speed_layout.addWidget(vx_label)
    speed_layout.addWidget(vx_input)
    speed_layout.addWidget(vy_label)
    speed_layout.addWidget(vy_input)
    speed_layout.addWidget(submit_btn)
    
    layout.addWidget(speed_group)
    
    # 定时器用于状态更新
    status_timer = QTimer()
    status_timer.timeout.connect(lambda: update_status_display())
    
    def update_status_display():
        """更新状态显示"""
        status = mouse_sim.get_status()
        
        # 更新详细信息
        info = f"""
运行状态: {'运行中' if status['running'] and status['thread_alive'] else '已停止'}
FPS: {status['fps']}
平滑系数: {status['smoothing']:.3f}
减速系数: {status['decay_rate']:.3f}
最大持续时间: {status['max_duration']:.3f}s
当前速度: X={status['current_velocity'][0]:.2f}, Y={status['current_velocity'][1]:.2f}
残差: X={status['residual'][0]:.3f}, Y={status['residual'][1]:.3f}
线程状态: {'活跃' if status['thread_alive'] else '已结束'}
        """
        info_text.setText(info.strip())
    
    # 按钮事件处理
    def on_start():
        """启动鼠标模拟器"""
        mouse_sim.start()
        status_timer.start(100)  # 每100ms更新一次状态
        print("🔄 启动鼠标模拟器")
    
    def on_stop():
        """停止鼠标模拟器"""
        mouse_sim.stop()
        print("🛑 停止鼠标模拟器")
    
    def on_reset():
        """重置鼠标模拟器"""
        mouse_sim.stop()
        mouse_sim.submit_vector(0, 0)  # 重置速度
        print("🔄 重置鼠标模拟器")
    
    def on_apply_params():
        """应用参数设置"""
        fps = int(fps_control.spinbox.value())
        smoothing = smoothing_control.spinbox.value()
        decay_rate = decay_control.spinbox.value()
        max_duration = duration_control.spinbox.value()
        
        mouse_sim.update_config(fps=fps, smoothing=smoothing)
        mouse_sim.update_decay_rate(decay_rate)
        mouse_sim.max_duration = max_duration
        
        print(f"✅ 应用参数: FPS={fps}, 平滑={smoothing:.3f}, 减速={decay_rate:.3f}, 持续时间={max_duration:.3f}s")
    
    def on_submit_speed():
        """提交速度向量"""
        vx = vx_input.value()
        vy = vy_input.value()
        mouse_sim.submit_vector(vx, vy)
        print(f"🎯 提交速度: X={vx}, Y={vy}")
    
    def on_refresh():
        """刷新状态"""
        update_status_display()
        print("🔄 刷新状态")
    
    # 连接按钮事件
    start_btn.clicked.connect(on_start)
    stop_btn.clicked.connect(on_stop)
    reset_btn.clicked.connect(on_reset)
    apply_btn.clicked.connect(on_apply_params)
    submit_btn.clicked.connect(on_submit_speed)
    refresh_btn.clicked.connect(on_refresh)
    
    # 设置快捷键
    start_shortcut = QShortcut(QKeySequence(Qt.Key_F4), group)
    start_shortcut.activated.connect(on_start)
    
    stop_shortcut = QShortcut(QKeySequence(Qt.Key_F5), group)
    stop_shortcut.activated.connect(on_stop)
    
    reset_shortcut = QShortcut(QKeySequence(Qt.Key_F6), group)
    reset_shortcut.activated.connect(on_reset)
    
    # 存储引用到组件
    group.status_timer = status_timer
    group.mouse_sim = mouse_sim
    group.info_text = info_text
    group.start_shortcut = start_shortcut
    group.stop_shortcut = stop_shortcut
    group.reset_shortcut = reset_shortcut
    
    return group


def get_mouse_control():
    """
    获取鼠标模拟器控制组件
    
    Returns:
        QGroupBox: 鼠标控制组件
    """
    return create_mouse_control()
