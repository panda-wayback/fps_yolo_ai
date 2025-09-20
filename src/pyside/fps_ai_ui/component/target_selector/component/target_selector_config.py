#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器配置组件
设置目标选择的各种权重参数
"""

from PySide6.QtWidgets import (QSlider, QLabel, QHBoxLayout, QVBoxLayout, 
                               QGroupBox, QSpinBox, QDoubleSpinBox, QPushButton, QWidget)
from PySide6.QtCore import Qt, Signal

try:
    from pyside.UI.basic.basic_layout import create_vertical_card
    from data_center.models.target_selector.subject import TargetSelectorSubject
except ImportError:
    # 直接运行时需要添加路径
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
    from pyside.UI.basic.basic_layout import create_vertical_card
    from data_center.models.target_selector.subject import TargetSelectorSubject


class WeightSlider(QWidget):
    """权重滑块组件"""
    
    def __init__(self, name: str, default_value: float = 0.5, parent=None):
        super().__init__(parent)
        self.name = name
        self.default_value = default_value
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
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(int(self.default_value * 100))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(25)
        layout.addWidget(self.slider)
        
        # 数值显示
        self.value_label = QLabel(f"{self.default_value:.2f}")
        self.value_label.setMinimumWidth(50)
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)
        
        # 连接信号
        self.slider.valueChanged.connect(self.on_slider_changed)
        
    def on_slider_changed(self, value):
        """滑块值改变时的处理"""
        float_value = value / 100.0
        self.value_label.setText(f"{float_value:.2f}")
        self.value_changed.emit(float_value)
        
    def get_value(self) -> float:
        """获取当前值"""
        return self.slider.value() / 100.0
        
    def set_value(self, value: float):
        """设置值"""
        self.slider.setValue(int(value * 100))
        
    # 信号
    value_changed = Signal(float)


class TargetSelectorConfigWidget(QGroupBox):
    """目标选择器配置组件"""
    
    def __init__(self, parent=None):
        super().__init__("目标选择器配置", parent)
        self.init_ui()
        self.load_current_config()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 距离权重
        self.distance_weight = WeightSlider("距离权重", 0.5)
        self.distance_weight.value_changed.connect(self.on_config_changed)
        layout.addWidget(self.distance_weight)
        
        # 置信度权重
        self.confidence_weight = WeightSlider("置信度权重", 0.5)
        self.confidence_weight.value_changed.connect(self.on_config_changed)
        layout.addWidget(self.confidence_weight)
        
        # 相似度权重
        self.similarity_weight = WeightSlider("相似度权重", 0.5)
        self.similarity_weight.value_changed.connect(self.on_config_changed)
        layout.addWidget(self.similarity_weight)
        
        # 类别权重
        self.class_weight = WeightSlider("类别权重", 0.5)
        self.class_weight.value_changed.connect(self.on_config_changed)
        layout.addWidget(self.class_weight)
        
        # 参考向量设置
        ref_group = QGroupBox("参考向量")
        ref_layout = QHBoxLayout(ref_group)
        
        ref_layout.addWidget(QLabel("X:"))
        self.ref_x_spinbox = QSpinBox()
        self.ref_x_spinbox.setRange(-1000, 1000)
        self.ref_x_spinbox.setValue(0)
        self.ref_x_spinbox.valueChanged.connect(self.on_config_changed)
        ref_layout.addWidget(self.ref_x_spinbox)
        
        ref_layout.addWidget(QLabel("Y:"))
        self.ref_y_spinbox = QSpinBox()
        self.ref_y_spinbox.setRange(-1000, 1000)
        self.ref_y_spinbox.setValue(0)
        self.ref_y_spinbox.valueChanged.connect(self.on_config_changed)
        ref_layout.addWidget(self.ref_y_spinbox)
        
        layout.addWidget(ref_group)
        
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
            state = TargetSelectorSubject.get_state()
            self.distance_weight.set_value(state.distance_weight)
            self.confidence_weight.set_value(state.confidence_weight)
            self.similarity_weight.set_value(state.similarity_weight)
            self.class_weight.set_value(state.class_weight)
            
            if state.reference_vector:
                self.ref_x_spinbox.setValue(int(state.reference_vector[0]))
                self.ref_y_spinbox.setValue(int(state.reference_vector[1]))
        except Exception as e:
            print(f"加载配置失败: {e}")
            
    def on_config_changed(self):
        """配置改变时的处理"""
        self.status_label.setText("配置已修改")
        self.status_label.setStyleSheet("color: orange; font-size: 10px;")
        
    def apply_config(self):
        """应用配置"""
        try:
            # 获取参考向量
            ref_vector = None
            if self.ref_x_spinbox.value() != 0 or self.ref_y_spinbox.value() != 0:
                ref_vector = (float(self.ref_x_spinbox.value()), float(self.ref_y_spinbox.value()))
            
            # 应用配置
            TargetSelectorSubject.set_config(
                distance_weight=self.distance_weight.get_value(),
                confidence_weight=self.confidence_weight.get_value(),
                similarity_weight=self.similarity_weight.get_value(),
                class_weight=self.class_weight.get_value(),
                reference_vector=ref_vector
            )
            
            self.status_label.setText("配置已保存")
            self.status_label.setStyleSheet("color: green; font-size: 10px;")
            
        except Exception as e:
            self.status_label.setText(f"保存失败: {str(e)}")
            self.status_label.setStyleSheet("color: red; font-size: 10px;")
            
    def reset_to_defaults(self):
        """重置为默认值"""
        self.distance_weight.set_value(0.5)
        self.confidence_weight.set_value(0.5)
        self.similarity_weight.set_value(0.5)
        self.class_weight.set_value(0.5)
        self.ref_x_spinbox.setValue(0)
        self.ref_y_spinbox.setValue(0)
        self.on_config_changed()


def create_target_selector_config():
    """
    创建目标选择器配置组件
    
    Returns:
        TargetSelectorConfigWidget: 目标选择器配置组件
    """
    return TargetSelectorConfigWidget()


if __name__ == "__main__":
    # 测试组件
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = create_target_selector_config()
    widget.show()
    
    sys.exit(app.exec())
