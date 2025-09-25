#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标驱动状态显示组件
显示鼠标驱动的运行状态和向量信息
"""

from PySide6.QtWidgets import QLabel, QProgressBar, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide6.QtCore import QTimer

from data_center.models.mouse_driver_model.state import MouseDriverState
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


class MouseDriverStateWidget(QGroupBox):
    """鼠标驱动状态显示组件"""
    
    def __init__(self, parent=None):
        super().__init__("鼠标驱动状态", parent)
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 运行状态
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("运行状态:"))
        self.status_label = QLabel("停止")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # 当前向量显示
        vector_group = QGroupBox("当前向量")
        vector_layout = QVBoxLayout(vector_group)
        
        # X向量
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X:"))
        self.x_label = QLabel("0.00")
        self.x_label.setStyleSheet("color: blue; font-weight: bold;")
        self.x_progress = QProgressBar()
        self.x_progress.setRange(-100, 100)
        self.x_progress.setValue(0)
        x_layout.addWidget(self.x_label)
        x_layout.addWidget(self.x_progress)
        vector_layout.addLayout(x_layout)
        
        # Y向量
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        self.y_label = QLabel("0.00")
        self.y_label.setStyleSheet("color: blue; font-weight: bold;")
        self.y_progress = QProgressBar()
        self.y_progress.setRange(-100, 100)
        self.y_progress.setValue(0)
        y_layout.addWidget(self.y_label)
        y_layout.addWidget(self.y_progress)
        vector_layout.addLayout(y_layout)
        
        layout.addWidget(vector_group)
        
        # 配置信息显示
        config_group = QGroupBox("当前配置")
        config_layout = QVBoxLayout(config_group)
        
        self.fps_label = QLabel("帧率: 1000 FPS")
        self.smoothing_label = QLabel("平滑系数: 0.40")
        self.duration_label = QLabel("最大持续时间: 0.05 秒")
        self.decay_label = QLabel("减速系数: 0.95")
        
        config_layout.addWidget(self.fps_label)
        config_layout.addWidget(self.smoothing_label)
        config_layout.addWidget(self.duration_label)
        config_layout.addWidget(self.decay_label)
        
        layout.addWidget(config_group)
        
        # 统计信息
        stats_group = QGroupBox("统计信息")
        stats_layout = QVBoxLayout(stats_group)
        
        self.vector_count_label = QLabel("向量发送次数: 0")
        self.last_update_label = QLabel("最后更新: 从未")
        
        stats_layout.addWidget(self.vector_count_label)
        stats_layout.addWidget(self.last_update_label)
        
        layout.addWidget(stats_group)
        
    def setup_timer(self):
        """设置定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)  # 每100ms更新一次
        
        # 统计变量
        self.vector_count = 0
        self.last_vector_time = None
        
    def update_status(self):
        """更新状态显示"""
        try:
            state = MouseDriverState.get_state()
            mouse_simulator = get_mouse_simulator()
            
            # 获取状态值
            running = mouse_simulator.is_running
            fps = state.fps.get()
            smoothing = state.smoothing.get()
            max_duration = state.max_duration.get()
            decay_rate = state.decay_rate.get()
            vector = state.vector.get()
            
            # 更新运行状态
            if running:
                self.status_label.setText("运行中")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.status_label.setText("停止")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
            
            # 更新向量显示
            vx = vector[0] if vector else 0.0
            vy = vector[1] if vector else 0.0
            
            self.x_label.setText(f"{vx:.2f}")
            self.y_label.setText(f"{vy:.2f}")
            
            # 更新进度条（限制在-100到100范围内）
            x_value = max(-100, min(100, int(vx)))
            y_value = max(-100, min(100, int(vy)))
            
            self.x_progress.setValue(x_value)
            self.y_progress.setValue(y_value)
            
            # 设置进度条颜色
            if abs(vx) > 0.1:
                self.x_progress.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
            else:
                self.x_progress.setStyleSheet("")
                
            if abs(vy) > 0.1:
                self.y_progress.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
            else:
                self.y_progress.setStyleSheet("")
            
            # 更新配置信息
            self.fps_label.setText(f"帧率: {fps} FPS")
            self.smoothing_label.setText(f"平滑系数: {smoothing:.2f}")
            self.duration_label.setText(f"最大持续时间: {max_duration:.3f} 秒")
            self.decay_label.setText(f"减速系数: {decay_rate:.2f}")
            
            # 更新统计信息
            if abs(vx) > 0.01 or abs(vy) > 0.01:
                self.vector_count += 1
                self.last_vector_time = "刚刚"
                
            self.vector_count_label.setText(f"向量发送次数: {self.vector_count}")
            self.last_update_label.setText(f"最后更新: {self.last_vector_time or '从未'}")
            
        except Exception as e:
            self.status_label.setText("错误")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            print(f"更新鼠标驱动状态失败: {e}")


def create_mouse_driver_state():
    """
    创建鼠标驱动状态显示组件
    
    Returns:
        MouseDriverStateWidget: 鼠标驱动状态显示组件
    """
    return MouseDriverStateWidget()


def get_mouse_driver_state():
    """
    获取鼠标驱动状态组件
    
    Returns:
        MouseDriverStateWidget: 鼠标驱动状态显示组件
    """
    return create_mouse_driver_state()


if __name__ == "__main__":
    # 测试组件
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = create_mouse_driver_state()
    widget.show()
    
    sys.exit(app.exec())
