#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器配置组件
设置PID控制器的各种参数
"""

from PySide6.QtWidgets import (QSlider, QLabel, QHBoxLayout, QVBoxLayout, 
                               QGroupBox, QPushButton, QWidget)
from PySide6.QtCore import Qt, Signal

from data_center.models.pid_model.subject import PIDSubject
from data_center.models.pid_model.state import PIDModelState


class ParameterSlider(QWidget):
    """参数滑块组件"""
    
    def __init__(self, name: str, min_val: float, max_val: float, default_value: float, 
                 step: float = 0.01, unit: str = "", parent=None):
        super().__init__(parent)
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.default_value = default_value
        self.step = step
        self.unit = unit
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标签
        self.label = QLabel(f"{self.name}:")
        self.label.setMinimumWidth(80)
        layout.addWidget(self.label)
        
        # 滑块
        self.slider = QSlider(Qt.Horizontal)
        slider_range = int((self.max_val - self.min_val) / self.step)
        self.slider.setMinimum(0)
        self.slider.setMaximum(slider_range)
        self.slider.setValue(int((self.default_value - self.min_val) / self.step))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(slider_range // 4)
        layout.addWidget(self.slider)
        
        # 数值显示
        self.value_label = QLabel(f"{self.default_value:.3f}{self.unit}")
        self.value_label.setMinimumWidth(80)
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        # 连接信号
        self.slider.valueChanged.connect(self._on_slider_changed)
        
    def _on_slider_changed(self, value):
        """滑块值改变时的处理"""
        actual_value = self.min_val + value * self.step
        self.value_label.setText(f"{actual_value:.3f}{self.unit}")
        self.value_changed.emit(actual_value)
    
    def get_value(self) -> float:
        """获取当前值"""
        return self.min_val + self.slider.value() * self.step
    
    def set_value(self, value: float):
        """设置值"""
        slider_value = int((value - self.min_val) / self.step)
        self.slider.setValue(slider_value)
        self.value_label.setText(f"{value:.3f}{self.unit}")
    
    # 信号
    value_changed = Signal(float)


class PIDConfigWidget(QGroupBox):
    """PID控制器配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("PID参数配置")
        self.setMinimumWidth(300)
        self.init_ui()
        self.load_current_values()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # Kp参数
        self.kp_slider = ParameterSlider("Kp", 0.0, 10.0, 1.0, 0.01, "")
        self.kp_slider.value_changed.connect(self._on_kp_changed)
        layout.addWidget(self.kp_slider)
        
        # Ki参数
        self.ki_slider = ParameterSlider("Ki", 0.0, 5.0, 0.1, 0.001, "")
        self.ki_slider.value_changed.connect(self._on_ki_changed)
        layout.addWidget(self.ki_slider)
        
        # Kd参数
        self.kd_slider = ParameterSlider("Kd", 0.0, 5.0, 0.1, 0.001, "")
        self.kd_slider.value_changed.connect(self._on_kd_changed)
        layout.addWidget(self.kd_slider)
        
        # 采样时间
        self.dt_slider = ParameterSlider("采样时间", 0.001, 0.1, 0.02, 0.001, "s")
        self.dt_slider.value_changed.connect(self._on_dt_changed)
        layout.addWidget(self.dt_slider)
        
        # 分隔线
        from PySide6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        
        # 重置按钮
        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_button)
        
        # 应用按钮
        self.apply_button = QPushButton("应用")
        self.apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(self.apply_button)
        
        # 保存按钮
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # 状态显示
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.status_label)
        
    def _on_kp_changed(self, value: float):
        """Kp参数改变"""
        self._update_status(f"Kp: {value:.3f}")
        
    def _on_ki_changed(self, value: float):
        """Ki参数改变"""
        self._update_status(f"Ki: {value:.3f}")
        
    def _on_kd_changed(self, value: float):
        """Kd参数改变"""
        self._update_status(f"Kd: {value:.3f}")
        
    def _on_dt_changed(self, value: float):
        """采样时间改变"""
        self._update_status(f"采样时间: {value:.3f}s")
        
    def _update_status(self, message: str):
        """更新状态显示"""
        self.status_label.setText(message)
        
    def reset_to_defaults(self):
        """重置为默认值"""
        self.kp_slider.set_value(1.0)
        self.ki_slider.set_value(0.1)
        self.kd_slider.set_value(0.1)
        self.dt_slider.set_value(0.02)
        self._update_status("已重置为默认值")
        
    def apply_settings(self):
        """应用设置"""
        try:
            kp = self.kp_slider.get_value()
            ki = self.ki_slider.get_value()
            kd = self.kd_slider.get_value()
            
            # 应用PID参数
            PIDSubject.set_pid_parameters(kp, ki, kd)
            
            self._update_status("设置已应用")
        except Exception as e:
            self._update_status(f"应用失败: {str(e)}")
            
    def save_settings(self):
        """保存设置"""
        try:
            # 这里可以添加保存到文件的逻辑
            self._update_status("设置已保存")
        except Exception as e:
            self._update_status(f"保存失败: {str(e)}")
            
    def load_current_values(self):
        """加载当前值"""
        try:
            state = PIDModelState.get_state()
            kp = state.kp.get()
            ki = state.ki.get()
            kd = state.kd.get()
            dt = state.dt.get()
            
            if kp is not None:
                self.kp_slider.set_value(kp)
            if ki is not None:
                self.ki_slider.set_value(ki)
            if kd is not None:
                self.kd_slider.set_value(kd)
            if dt is not None:
                self.dt_slider.set_value(dt)
                
        except Exception as e:
            print(f"加载当前值失败: {e}")


def create_pid_config():
    """创建PID配置组件"""
    return PIDConfigWidget()
