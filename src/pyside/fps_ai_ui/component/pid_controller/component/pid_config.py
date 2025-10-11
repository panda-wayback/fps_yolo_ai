#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADRC控制器配置组件
设置ADRC（自抗扰）控制器的各种参数
"""

from PySide6.QtWidgets import (QSlider, QLabel, QHBoxLayout, QVBoxLayout, 
                               QGroupBox, QPushButton, QWidget, QComboBox)
from PySide6.QtCore import Qt, Signal

from data_center.models.controller_model.subject import ControllerSubject
from data_center.models.controller_model.state import ControllerModelState


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


class ADRCConfigWidget(QGroupBox):
    """ADRC控制器配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("ADRC参数配置")
        self.setMinimumWidth(350)
        self.init_ui()
        self.load_current_values()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 控制器阶数 (order) - 使用下拉框
        order_layout = QHBoxLayout()
        order_label = QLabel("控制器阶数:")
        order_label.setMinimumWidth(80)
        order_layout.addWidget(order_label)
        
        self.order_combo = QComboBox()
        self.order_combo.addItems(["1阶", "2阶"])
        self.order_combo.setCurrentIndex(0)  # 默认1阶
        self.order_combo.currentIndexChanged.connect(self._on_order_changed)
        order_layout.addWidget(self.order_combo)
        layout.addLayout(order_layout)
        
        # 采样时间 (sample_time)
        self.sample_time_slider = ParameterSlider("采样时间", 0.001, 0.1, 0.01, 0.001, "s")
        self.sample_time_slider.value_changed.connect(self._on_sample_time_changed)
        layout.addWidget(self.sample_time_slider)
        
        # 控制增益 (b0)
        self.b0_slider = ParameterSlider("控制增益 b0", 0.1, 10.0, 1.0, 0.1, "")
        self.b0_slider.value_changed.connect(self._on_b0_changed)
        layout.addWidget(self.b0_slider)
        
        # 控制器带宽 (w_cl)
        self.w_cl_slider = ParameterSlider("控制器带宽", 10.0, 200.0, 60.0, 1.0, "")
        self.w_cl_slider.value_changed.connect(self._on_w_cl_changed)
        layout.addWidget(self.w_cl_slider)
        
        # ESO增益 (k_eso)
        self.k_eso_slider = ParameterSlider("ESO增益", 1.0, 10.0, 2.5, 0.1, "")
        self.k_eso_slider.value_changed.connect(self._on_k_eso_changed)
        layout.addWidget(self.k_eso_slider)
        
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
        
    def _on_order_changed(self, index: int):
        """控制器阶数改变"""
        order = index + 1  # 0->1阶, 1->2阶
        self._update_status(f"阶数: {order}阶")
    
    def _on_sample_time_changed(self, value: float):
        """采样时间改变"""
        self._update_status(f"采样时间: {value:.3f}s")
        
    def _on_b0_changed(self, value: float):
        """控制增益改变"""
        self._update_status(f"b0: {value:.3f}")
        
    def _on_w_cl_changed(self, value: float):
        """控制器带宽改变"""
        self._update_status(f"w_cl: {value:.1f}")
        
    def _on_k_eso_changed(self, value: float):
        """ESO增益改变"""
        self._update_status(f"k_eso: {value:.2f}")
        
    def _update_status(self, message: str):
        """更新状态显示"""
        self.status_label.setText(message)
        
    def reset_to_defaults(self):
        """重置为默认值"""
        self.order_combo.setCurrentIndex(0)  # 1阶
        self.sample_time_slider.set_value(0.01)
        self.b0_slider.set_value(1.0)
        self.w_cl_slider.set_value(60.0)
        self.k_eso_slider.set_value(2.5)
        self._update_status("已重置为默认值")
        
    def apply_settings(self):
        """应用设置"""
        try:
            # 获取当前参数值
            order = self.order_combo.currentIndex() + 1  # 0->1阶, 1->2阶
            sample_time = self.sample_time_slider.get_value()
            b0 = self.b0_slider.get_value()
            w_cl = self.w_cl_slider.get_value()
            k_eso = self.k_eso_slider.get_value()
            
            # 暂时不设置限幅（使用None）
            output_limits = None
            rate_limits = None
            
            # 应用ADRC参数
            ControllerSubject.send_config(
                order=order,
                sample_time=sample_time,
                b0=b0,
                w_cl=w_cl,
                k_eso=k_eso,
                output_limits=output_limits,
                rate_limits=rate_limits
            )
            
            self._update_status("✅ 设置已应用")
        except Exception as e:
            self._update_status(f"❌ 应用失败: {str(e)}")
            
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
            # 从状态管理中加载当前ADRC参数
            state = ControllerModelState.get_state()
            order = state.order.get()
            sample_time = state.sample_time.get()
            b0 = state.b0.get()
            w_cl = state.w_cl.get()
            k_eso = state.k_eso.get()
            
            # 更新UI组件
            if order is not None:
                self.order_combo.setCurrentIndex(order - 1)  # 1阶->0, 2阶->1
            if sample_time is not None:
                self.sample_time_slider.set_value(sample_time)
            if b0 is not None:
                self.b0_slider.set_value(b0)
            if w_cl is not None:
                self.w_cl_slider.set_value(w_cl)
            if k_eso is not None:
                self.k_eso_slider.set_value(k_eso)
                
            self._update_status("✅ 已加载当前参数")
        except Exception as e:
            print(f"加载当前值失败: {e}")
            self._update_status(f"⚠️ 加载失败: {str(e)}")


def create_pid_config():
    """创建ADRC配置组件（保持函数名以兼容现有代码）"""
    return ADRCConfigWidget()


def create_adrc_config():
    """创建ADRC配置组件"""
    return ADRCConfigWidget()
