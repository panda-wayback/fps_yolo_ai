#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标驱动配置组件
设置鼠标驱动的各种参数
"""

from PySide6.QtWidgets import (QSlider, QLabel, QHBoxLayout, QVBoxLayout, 
                               QGroupBox, QPushButton, QWidget)
from PySide6.QtCore import Qt, Signal

from data_center.models.mouse_driver_model.subject import MouseDriverSubject
from data_center.models.mouse_driver_model.state import MouseDriverState


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
        self.label.setMinimumWidth(100)
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
        self.value_label = QLabel(f"{self.default_value:.2f}{self.unit}")
        self.value_label.setMinimumWidth(80)
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        # 连接信号
        self.slider.valueChanged.connect(self.on_slider_changed)
        
    def on_slider_changed(self, value):
        """滑块值改变时的处理"""
        float_value = self.min_val + value * self.step
        self.value_label.setText(f"{float_value:.2f}{self.unit}")
        self.value_changed.emit(float_value)
        
    def get_value(self) -> float:
        """获取当前值"""
        return self.min_val + self.slider.value() * self.step
        
    def set_value(self, value: float):
        """设置值"""
        slider_value = int((value - self.min_val) / self.step)
        self.slider.setValue(slider_value)
        
    # 信号
    value_changed = Signal(float)


class MouseDriverConfigWidget(QGroupBox):
    """鼠标驱动配置组件"""
    
    def __init__(self, parent=None):
        super().__init__("鼠标驱动配置", parent)
        self.init_ui()
        self.load_current_config()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        
        # 性能参数
        perf_group = QGroupBox("性能参数")
        perf_layout = QVBoxLayout(perf_group)
        
        # FPS设置
        self.fps_slider = ParameterSlider("帧率", 10, 2000, 1000, 10, " FPS")
        self.fps_slider.value_changed.connect(self.on_config_changed)
        perf_layout.addWidget(self.fps_slider)
        
        # 平滑系数
        self.smoothing_slider = ParameterSlider("平滑系数", 0.0, 1.0, 0.4, 0.01)
        self.smoothing_slider.value_changed.connect(self.on_config_changed)
        perf_layout.addWidget(self.smoothing_slider)
        
        layout.addWidget(perf_group)
        
        # 运动参数
        motion_group = QGroupBox("运动参数")
        motion_layout = QVBoxLayout(motion_group)
        
        # 最大持续时间
        self.max_duration_slider = ParameterSlider("最大持续时间", 0.001, 0.2, 0.05, 0.001, " 秒")
        self.max_duration_slider.value_changed.connect(self.on_config_changed)
        motion_layout.addWidget(self.max_duration_slider)
        
        # 减速系数
        self.decay_rate_slider = ParameterSlider("减速系数", 0.5, 0.99, 0.95, 0.01)
        self.decay_rate_slider.value_changed.connect(self.on_config_changed)
        motion_layout.addWidget(self.decay_rate_slider)
        
        layout.addWidget(motion_group)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        
        # 重置按钮
        self.reset_btn = QPushButton("重置默认值")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        # 应用按钮
        self.apply_btn = QPushButton("应用配置")
        self.apply_btn.clicked.connect(self.apply_config)
        self.apply_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        button_layout.addWidget(self.apply_btn)
        
        layout.addLayout(button_layout)
        
        # 状态显示
        self.status_label = QLabel("配置已保存")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: green; font-size: 10px;")
        layout.addWidget(self.status_label)
        
    def load_current_config(self):
        """加载当前配置"""
        try:
            state = MouseDriverState.get_state()
            self.fps_slider.set_value(state.fps.get())
            self.smoothing_slider.set_value(state.smoothing.get())
            self.max_duration_slider.set_value(state.max_duration.get())
            self.decay_rate_slider.set_value(state.decay_rate.get())
        except Exception as e:
            print(f"加载配置失败: {e}")
            
    def on_config_changed(self):
        """配置改变时的处理"""
        self.status_label.setText("配置已修改")
        self.status_label.setStyleSheet("color: orange; font-size: 10px;")
        
    def apply_config(self):
        """应用配置"""
        try:
            MouseDriverSubject.send_config(
                fps=int(self.fps_slider.get_value()),
                smoothing=self.smoothing_slider.get_value(),
                max_duration=self.max_duration_slider.get_value(),
                decay_rate=self.decay_rate_slider.get_value()
            )
            
            self.status_label.setText("配置已保存")
            self.status_label.setStyleSheet("color: green; font-size: 10px;")
            
        except Exception as e:
            self.status_label.setText(f"保存失败: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 10px;")
            
    def reset_to_defaults(self):
        """重置为默认值"""
        self.fps_slider.set_value(1000)
        self.smoothing_slider.set_value(0.4)
        self.max_duration_slider.set_value(0.05)
        self.decay_rate_slider.set_value(0.95)
        self.on_config_changed()


def create_mouse_driver_config():
    """
    创建鼠标驱动配置组件
    
    Returns:
        MouseDriverConfigWidget: 鼠标驱动配置组件
    """
    return MouseDriverConfigWidget()


if __name__ == "__main__":
    # 测试组件
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = create_mouse_driver_config()
    widget.show()
    
    sys.exit(app.exec())
