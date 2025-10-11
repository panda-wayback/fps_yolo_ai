#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADRC控制器状态显示组件
显示ADRC（自抗扰）控制器的实时状态和输出
"""

from PySide6.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QWidget, QProgressBar, QTextEdit, QPushButton)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from data_center.models.controller_model.state import ControllerModelState


class StatusDisplayWidget(QWidget):
    """状态显示组件"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 数值显示
        self.value_label = QLabel("0.000")
        self.value_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("color: #2E8B57; background-color: #F0F8FF; border: 1px solid #4682B4; border-radius: 5px; padding: 5px;")
        layout.addWidget(self.value_label)
        
    def update_value(self, value: float):
        """更新数值显示"""
        self.value_label.setText(f"{value:.3f}")


class ADRCStateWidget(QGroupBox):
    """ADRC状态显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("ADRC状态监控")
        self.setMinimumWidth(300)
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 当前参数显示
        params_group = QGroupBox("当前参数")
        params_layout = QVBoxLayout(params_group)
        
        # 控制器阶数 (order)
        order_layout = QHBoxLayout()
        order_layout.addWidget(QLabel("阶数:"))
        self.order_label = QLabel("1阶")
        self.order_label.setStyleSheet("font-weight: bold; color: #2E8B57;")
        order_layout.addWidget(self.order_label)
        order_layout.addStretch()
        params_layout.addLayout(order_layout)
        
        # 采样时间 (sample_time)
        sample_time_layout = QHBoxLayout()
        sample_time_layout.addWidget(QLabel("采样时间:"))
        self.sample_time_label = QLabel("0.010s")
        self.sample_time_label.setStyleSheet("font-weight: bold; color: #2E8B57;")
        sample_time_layout.addWidget(self.sample_time_label)
        sample_time_layout.addStretch()
        params_layout.addLayout(sample_time_layout)
        
        # 控制增益 (b0)
        b0_layout = QHBoxLayout()
        b0_layout.addWidget(QLabel("控制增益 b0:"))
        self.b0_label = QLabel("1.000")
        self.b0_label.setStyleSheet("font-weight: bold; color: #2E8B57;")
        b0_layout.addWidget(self.b0_label)
        b0_layout.addStretch()
        params_layout.addLayout(b0_layout)
        
        # 控制器带宽 (w_cl)
        w_cl_layout = QHBoxLayout()
        w_cl_layout.addWidget(QLabel("控制器带宽:"))
        self.w_cl_label = QLabel("60.0")
        self.w_cl_label.setStyleSheet("font-weight: bold; color: #2E8B57;")
        w_cl_layout.addWidget(self.w_cl_label)
        w_cl_layout.addStretch()
        params_layout.addLayout(w_cl_layout)
        
        # ESO增益 (k_eso)
        k_eso_layout = QHBoxLayout()
        k_eso_layout.addWidget(QLabel("ESO增益:"))
        self.k_eso_label = QLabel("2.5")
        self.k_eso_label.setStyleSheet("font-weight: bold; color: #2E8B57;")
        k_eso_layout.addWidget(self.k_eso_label)
        k_eso_layout.addStretch()
        params_layout.addLayout(k_eso_layout)
        
        layout.addWidget(params_group)
        
        # 分隔线
        from PySide6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # 实时输出显示
        output_group = QGroupBox("实时输出")
        output_layout = QVBoxLayout(output_group)
        
        # X轴输出
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X轴输出:"))
        self.x_output_display = StatusDisplayWidget("X轴")
        x_layout.addWidget(self.x_output_display)
        output_layout.addLayout(x_layout)
        
        # Y轴输出
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y轴输出:"))
        self.y_output_display = StatusDisplayWidget("Y轴")
        y_layout.addWidget(self.y_output_display)
        output_layout.addLayout(y_layout)
        
        layout.addWidget(output_group)
        
        # 分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator2)
        
        # 控制状态
        control_group = QGroupBox("控制状态")
        control_layout = QVBoxLayout(control_group)
        
        # 是否启用
        self.enabled_label = QLabel("状态: 未启用")
        self.enabled_label.setAlignment(Qt.AlignCenter)
        self.enabled_label.setStyleSheet("color: red; font-weight: bold; background-color: #FFE4E1; border: 1px solid #FF6B6B; border-radius: 5px; padding: 5px;")
        control_layout.addWidget(self.enabled_label)
        
        # 输出强度条
        intensity_layout = QHBoxLayout()
        intensity_layout.addWidget(QLabel("输出强度:"))
        self.intensity_bar = QProgressBar()
        self.intensity_bar.setRange(0, 100)
        self.intensity_bar.setValue(0)
        self.intensity_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #4682B4;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #32CD32;
                border-radius: 4px;
            }
        """)
        intensity_layout.addWidget(self.intensity_bar)
        control_layout.addLayout(intensity_layout)
        
        layout.addWidget(control_group)
        
        # 分隔线
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator3)
        
        # 日志显示
        log_group = QGroupBox("控制日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(100)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        # 清空日志按钮
        clear_button = QPushButton("清空日志")
        clear_button.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_button)
        
        layout.addWidget(log_group)
        
    def setup_timer(self):
        """设置定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # 每100ms更新一次
        
    def update_display(self):
        """更新显示"""
        try:
            # 从 ControllerModelState 获取状态
            state = ControllerModelState.get_state()
            
            # 更新ADRC参数显示
            order = state.order.get()
            sample_time = state.sample_time.get()
            b0 = state.b0.get()
            w_cl = state.w_cl.get()
            k_eso = state.k_eso.get()
            
            if order is not None:
                self.order_label.setText(f"{order}阶")
            if sample_time is not None:
                self.sample_time_label.setText(f"{sample_time:.3f}s")
            if b0 is not None:
                self.b0_label.setText(f"{b0:.3f}")
            if w_cl is not None:
                self.w_cl_label.setText(f"{w_cl:.1f}")
            if k_eso is not None:
                self.k_eso_label.setText(f"{k_eso:.2f}")
            
            # 更新输出显示
            output = state.output.get()
            if output is not None and len(output) >= 2:
                x_output, y_output = output[0], output[1]
                self.x_output_display.update_value(x_output)
                self.y_output_display.update_value(y_output)
            
            # 更新控制状态（检查是否有 is_enabled 字段）
            if hasattr(state, 'is_enabled'):
                is_enabled = state.is_enabled.get()
                if is_enabled:
                    self.enabled_label.setText("状态: 已启用")
                    self.enabled_label.setStyleSheet("color: green; font-weight: bold; background-color: #E8F5E8; border: 1px solid #32CD32; border-radius: 5px; padding: 5px;")
                else:
                    self.enabled_label.setText("状态: 未启用")
                    self.enabled_label.setStyleSheet("color: red; font-weight: bold; background-color: #FFE4E1; border: 1px solid #FF6B6B; border-radius: 5px; padding: 5px;")
            else:
                # 如果没有 is_enabled 字段，根据输出判断
                if output is not None:
                    self.enabled_label.setText("状态: 运行中")
                    self.enabled_label.setStyleSheet("color: green; font-weight: bold; background-color: #E8F5E8; border: 1px solid #32CD32; border-radius: 5px; padding: 5px;")
                else:
                    self.enabled_label.setText("状态: 待机")
                    self.enabled_label.setStyleSheet("color: orange; font-weight: bold; background-color: #FFF8E1; border: 1px solid #FFA500; border-radius: 5px; padding: 5px;")
            
            # 更新输出强度条
            if output is not None and len(output) >= 2:
                x_output, y_output = output[0], output[1]
                intensity = min(100, max(0, int(abs(x_output) + abs(y_output)) * 10))
                self.intensity_bar.setValue(intensity)
            
        except Exception as e:
            self.add_log(f"更新显示错误: {e}")
            
    def add_log(self, message: str):
        """添加日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.log_text.append(log_message)
        
        # 限制日志行数
        if self.log_text.document().blockCount() > 50:
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.select(cursor.SelectionType.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()
            
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()


def create_pid_state():
    """创建ADRC状态显示组件（保持函数名以兼容现有代码）"""
    return ADRCStateWidget()


def create_adrc_state():
    """创建ADRC状态显示组件"""
    return ADRCStateWidget()
