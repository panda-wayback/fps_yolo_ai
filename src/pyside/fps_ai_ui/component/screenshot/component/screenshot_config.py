#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图设置组件
设置截图区域和参数
"""

from PySide6.QtWidgets import (QSpinBox, QLabel, QHBoxLayout, 
                               QVBoxLayout, QPushButton, QGroupBox)
from PySide6.QtCore import QThread, Signal
from pyside.UI.basic.basic_layout import create_vertical_card

from data_center.models.screenshot.subject import ScreenshotSubject
from data_center.models.screenshot.state import ScreenshotModelState
from singleton_classes.screenshot_img.main import get_screenshot
from utils.move_mouse.move_mouse import get_mouse_position
import time


class MousePositionMonitor(QThread):
    """鼠标位置监控线程"""
    position_found = Signal(int, int)  # 发送找到的稳定位置
    status_update = Signal(str)  # 发送状态更新
    
    def __init__(self, duration=10, stability_threshold=3):
        super().__init__()
        self.duration = duration  # 监控持续时间（秒）
        self.stability_threshold = stability_threshold  # 稳定阈值（秒）
        self.running = False
        
    def run(self):
        """运行监控线程"""
        self.running = True
        self.status_update.emit("🔍 开始监控鼠标位置...")
        
        start_time = time.time()
        last_position = None
        stable_start_time = None
        
        while self.running and (time.time() - start_time) < self.duration:
            try:
                current_pos = get_mouse_position()
                
                if last_position is None:
                    last_position = current_pos
                    stable_start_time = time.time()
                    self.status_update.emit(f"📍 当前位置: {current_pos}")
                elif current_pos == last_position:
                    # 位置相同，检查是否稳定足够长时间
                    stable_duration = time.time() - stable_start_time
                    if stable_duration >= self.stability_threshold:
                        # 位置稳定，发送结果
                        self.position_found.emit(current_pos[0], current_pos[1])
                        self.status_update.emit(f"✅ 位置稳定: {current_pos}")
                        self.running = False
                        return
                    else:
                        remaining = self.stability_threshold - stable_duration
                        self.status_update.emit(f"⏳ 位置稳定中... ({remaining:.1f}s)")
                else:
                    # 位置变化，重新开始计时
                    last_position = current_pos
                    stable_start_time = time.time()
                    self.status_update.emit(f"📍 位置变化: {current_pos}")
                
                time.sleep(0.1)  # 100ms检查一次
                
            except Exception as e:
                self.status_update.emit(f"❌ 监控错误: {str(e)}")
                time.sleep(0.1)
        
        if self.running:
            self.status_update.emit("⏰ 监控超时，未找到稳定位置")
        
        self.running = False
    
    def stop(self):
        """停止监控"""
        self.running = False


def create_screenshot_config():
    """
    创建截图设置组件
    
    Returns:
        QGroupBox: 截图设置组件
    """
    # 创建主容器
    group = create_vertical_card("截图设置")
    layout = group._layout
    
    # 鼠标位置设置
    mouse_group = QGroupBox("鼠标位置")
    mouse_layout = QVBoxLayout(mouse_group)
    
    # X坐标
    x_layout = QHBoxLayout()
    x_layout.addWidget(QLabel("X坐标:"))
    x_spinbox = QSpinBox()
    x_spinbox.setRange(0, 9999)
    x_spinbox.setValue(960)  # 默认屏幕中心X
    x_layout.addWidget(x_spinbox)
    mouse_layout.addLayout(x_layout)
    
    # Y坐标
    y_layout = QHBoxLayout()
    y_layout.addWidget(QLabel("Y坐标:"))
    y_spinbox = QSpinBox()
    y_spinbox.setRange(0, 9999)
    y_spinbox.setValue(540)  # 默认屏幕中心Y
    y_layout.addWidget(y_spinbox)
    mouse_layout.addLayout(y_layout)
    
    # 截图区域设置
    region_group = QGroupBox("截图区域")
    region_layout = QVBoxLayout(region_group)
    
    # 宽度
    width_layout = QHBoxLayout()
    width_layout.addWidget(QLabel("宽度:"))
    width_spinbox = QSpinBox()
    width_spinbox.setRange(50, 2000)
    width_spinbox.setValue(640)  # 默认宽度
    width_layout.addWidget(width_spinbox)
    region_layout.addLayout(width_layout)
    
    # 高度
    height_layout = QHBoxLayout()
    height_layout.addWidget(QLabel("高度:"))
    height_spinbox = QSpinBox()
    height_spinbox.setRange(50, 2000)
    height_spinbox.setValue(480)  # 默认高度
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
    fps_spinbox.setValue(60)  # 默认60FPS
    fps_time_layout.addWidget(fps_spinbox)
    fps_layout.addLayout(fps_time_layout)
    
    # 按钮区域
    button_layout = QHBoxLayout()
    
    # 应用设置按钮
    apply_btn = QPushButton("应用设置")
    
    # 重置按钮
    reset_btn = QPushButton("重置")
    
    # 获取当前鼠标位置按钮
    get_mouse_btn = QPushButton("获取鼠标位置")
    
    # 监控状态标签
    monitor_label = QLabel("点击按钮开始10秒监控")
    monitor_label.setStyleSheet("color: gray; font-size: 10px;")
    
    button_layout.addWidget(apply_btn)
    button_layout.addWidget(reset_btn)
    button_layout.addWidget(get_mouse_btn)
    
    # 状态标签
    status_label = QLabel("就绪")
    status_label.setStyleSheet("color: green; font-size: 12px;")
    
    # 当前配置显示标签
    config_label = QLabel("")
    config_label.setStyleSheet("color: blue; font-size: 10px;")
    config_label.setWordWrap(True)
    
    # 监控线程引用
    monitor_thread = None
    
    # 更新配置显示
    def update_config_display():
        """更新当前配置显示"""
        try:
            screenshot_state = ScreenshotModelState.get_state()
            
            mouse_pos = screenshot_state.mouse_pos.get()
            region_size = screenshot_state.region_size.get()
            fps = screenshot_state.fps.get()
            is_running = screenshot_state.is_running.get()
            
            if mouse_pos and region_size and fps is not None:
                config_text = f"当前配置: 位置={mouse_pos}, 区域={region_size}, FPS={fps}"
                if is_running:
                    config_text += " [运行中]"
                else:
                    config_text += " [已停止]"
                config_label.setText(config_text)
            else:
                config_label.setText("当前配置: 未设置")
                
        except Exception as e:
            config_label.setText(f"配置显示错误: {str(e)}")
    
    # 应用设置功能
    def apply_settings():
        """应用截图设置"""
        try:
            mouse_pos = (x_spinbox.value(), y_spinbox.value())
            region_size = (width_spinbox.value(), height_spinbox.value())
            fps = fps_spinbox.value()
            
            ScreenshotSubject.send_config(mouse_pos, region_size, fps)

            # 启动截图
            get_screenshot().start()
            
            # 更新配置显示
            update_config_display()
            
            status_label.setText("✅ 设置已应用")
            status_label.setStyleSheet("color: green; font-size: 12px;")
            print(f"✅ 截图设置已应用: 位置={mouse_pos}, 区域={region_size}, FPS={fps}")
            
        except Exception as e:
            status_label.setText(f"❌ 设置失败: {str(e)}")
            status_label.setStyleSheet("color: red; font-size: 12px;")
            print(f"❌ 应用设置失败: {str(e)}")
    
    # 重置功能
    def reset_settings():
        """重置为默认设置"""
        x_spinbox.setValue(756)
        y_spinbox.setValue(509)
        width_spinbox.setValue(400)
        height_spinbox.setValue(320)
        fps_spinbox.setValue(1000)
        
        status_label.setText("🔄 已重置为默认设置")
        status_label.setStyleSheet("color: orange; font-size: 12px;")
        print("🔄 已重置为默认设置")
    
    # 获取鼠标位置功能
    def get_mouse_position_click():
        """开始监控鼠标位置"""
        nonlocal monitor_thread
        
        # 如果已有监控线程在运行，先停止
        if monitor_thread and monitor_thread.isRunning():
            monitor_thread.stop()
            monitor_thread.wait()
        
        # 创建新的监控线程
        monitor_thread = MousePositionMonitor(duration=10, stability_threshold=3)
        
        # 连接信号
        monitor_thread.position_found.connect(on_position_found)
        monitor_thread.status_update.connect(on_status_update)
        monitor_thread.finished.connect(on_monitor_finished)
        
        # 禁用按钮，防止重复点击
        get_mouse_btn.setEnabled(False)
        get_mouse_btn.setText("监控中...")
        
        # 启动监控
        monitor_thread.start()
    
    def on_position_found(x, y):
        """当找到稳定位置时的回调"""
        x_spinbox.setValue(x)
        y_spinbox.setValue(y)
        
        status_label.setText(f"✅ 位置已设置: ({x}, {y})")
        status_label.setStyleSheet("color: green; font-size: 12px;")
        print(f"✅ 鼠标位置已设置: ({x}, {y})")
    
    def on_status_update(message):
        """状态更新回调"""
        monitor_label.setText(message)
        print(f"监控状态: {message}")
    
    def on_monitor_finished():
        """监控完成回调"""
        get_mouse_btn.setEnabled(True)
        get_mouse_btn.setText("获取鼠标位置")
        
        if not monitor_thread.running:
            monitor_label.setText("监控完成")
        else:
            monitor_label.setText("监控超时，请重试")
    
    # 连接按钮事件
    apply_btn.clicked.connect(apply_settings)
    reset_btn.clicked.connect(reset_settings)
    get_mouse_btn.clicked.connect(get_mouse_position_click)
    
    
    # 添加到布局
    layout.addWidget(mouse_group)
    layout.addWidget(region_group)
    layout.addWidget(fps_group)
    layout.addLayout(button_layout)
    layout.addWidget(monitor_label)
    layout.addWidget(config_label)
    layout.addWidget(status_label)
    
    # 初始化时更新配置显示
    update_config_display()
    
    # 存储引用
    group.apply_settings = apply_settings
    group.reset_settings = reset_settings
    group.get_mouse_position = get_mouse_position
    
    return group


def get_screenshot_config():
    """
    获取截图设置组件
    
    Returns:
        QGroupBox: 截图设置组件
    """
    return create_screenshot_config()
