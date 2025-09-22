#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器状态显示组件
显示当前选中的目标信息
"""

from PySide6.QtWidgets import (QLabel, QVBoxLayout, QGroupBox, QGridLayout,
                               QProgressBar, QFrame)
from PySide6.QtCore import Qt, QTimer

try:
    from pyside.UI.basic.basic_layout import create_vertical_card
    from data_center.models.target_selector.subject import TargetSelectorSubject
    from data_center.models.target_selector.state import TargetSelectorState
except ImportError:
    # 直接运行时需要添加路径
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
    from pyside.UI.basic.basic_layout import create_vertical_card
    from data_center.models.target_selector.subject import TargetSelectorSubject
    from data_center.models.target_selector.state import TargetSelectorState


class TargetSelectorStateWidget(QGroupBox):
    """目标选择器状态显示组件"""
    
    def __init__(self, parent=None):
        super().__init__("目标选择状态", parent)
        self.init_ui()
        self.init_timer()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 目标信息显示区域
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setLineWidth(1)
        info_layout = QGridLayout(info_frame)
        
        # 选中状态
        self.status_label = QLabel("未选中目标")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        info_layout.addWidget(QLabel("状态:"), 0, 0)
        info_layout.addWidget(self.status_label, 0, 1)
        
        # 目标中心点
        self.center_label = QLabel("N/A")
        info_layout.addWidget(QLabel("中心点:"), 1, 0)
        info_layout.addWidget(self.center_label, 1, 1)
        
        # 目标边界框
        self.bbox_label = QLabel("N/A")
        info_layout.addWidget(QLabel("边界框:"), 2, 0)
        info_layout.addWidget(self.bbox_label, 2, 1)
        
        # 置信度
        self.confidence_label = QLabel("N/A")
        info_layout.addWidget(QLabel("置信度:"), 3, 0)
        info_layout.addWidget(self.confidence_label, 3, 1)
        
        # 置信度进度条
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setVisible(False)
        info_layout.addWidget(QLabel(""), 4, 0)
        info_layout.addWidget(self.confidence_bar, 4, 1)
        
        # 类别ID
        self.class_label = QLabel("N/A")
        info_layout.addWidget(QLabel("类别ID:"), 5, 0)
        info_layout.addWidget(self.class_label, 5, 1)
        
        layout.addWidget(info_frame)
        
        # 当前配置显示
        config_frame = QFrame()
        config_frame.setFrameStyle(QFrame.Box)
        config_frame.setLineWidth(1)
        config_layout = QGridLayout(config_frame)
        
        config_layout.addWidget(QLabel("当前配置:"), 0, 0, 1, 2)
        
        # 权重显示
        self.distance_weight_label = QLabel("0.50")
        self.confidence_weight_label = QLabel("0.50")
        self.similarity_weight_label = QLabel("0.50")
        self.class_weight_label = QLabel("0.50")
        
        config_layout.addWidget(QLabel("距离权重:"), 1, 0)
        config_layout.addWidget(self.distance_weight_label, 1, 1)
        config_layout.addWidget(QLabel("置信度权重:"), 2, 0)
        config_layout.addWidget(self.confidence_weight_label, 2, 1)
        config_layout.addWidget(QLabel("相似度权重:"), 3, 0)
        config_layout.addWidget(self.similarity_weight_label, 3, 1)
        config_layout.addWidget(QLabel("类别权重:"), 4, 0)
        config_layout.addWidget(self.class_weight_label, 4, 1)
        
        layout.addWidget(config_frame)
        
        # 更新时间显示
        self.update_time_label = QLabel("")
        self.update_time_label.setAlignment(Qt.AlignCenter)
        self.update_time_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.update_time_label)
        
    def init_timer(self):
        """初始化定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(100)  # 每100ms更新一次
        
    def update_state(self):
        """更新状态显示"""
        try:
            state = TargetSelectorState.get_state()
            
            # 获取状态值
            selected_target_point = state.selected_target_point.get()
            selected_target_bbox = state.selected_target_bbox.get()
            selected_target_confidence = state.selected_target_confidence.get()
            selected_target_class_id = state.selected_target_class_id.get()
            
            # 更新目标信息
            if selected_target_point:
                self.status_label.setText("已选中目标")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                
                # 中心点
                center_text = f"({selected_target_point[0]:.1f}, {selected_target_point[1]:.1f})"
                self.center_label.setText(center_text)
                
                # 边界框
                if selected_target_bbox:
                    bbox_text = f"({selected_target_bbox[0]:.0f}, {selected_target_bbox[1]:.0f}, {selected_target_bbox[2]:.0f}, {selected_target_bbox[3]:.0f})"
                    self.bbox_label.setText(bbox_text)
                else:
                    self.bbox_label.setText("N/A")
                
                # 置信度
                if selected_target_confidence is not None:
                    conf_text = f"{selected_target_confidence:.3f}"
                    self.confidence_label.setText(conf_text)
                    self.confidence_bar.setValue(int(selected_target_confidence * 100))
                    self.confidence_bar.setVisible(True)
                else:
                    self.confidence_label.setText("N/A")
                    self.confidence_bar.setVisible(False)
                
                # 类别ID
                if selected_target_class_id is not None:
                    self.class_label.setText(str(selected_target_class_id))
                else:
                    self.class_label.setText("N/A")
                    
            else:
                self.status_label.setText("未选中目标")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
                self.center_label.setText("N/A")
                self.bbox_label.setText("N/A")
                self.confidence_label.setText("N/A")
                self.class_label.setText("N/A")
                self.confidence_bar.setVisible(False)
            
            # 更新配置显示
            self.distance_weight_label.setText(f"{state.distance_weight.get():.2f}")
            self.confidence_weight_label.setText(f"{state.confidence_weight.get():.2f}")
            self.similarity_weight_label.setText(f"{state.similarity_weight.get():.2f}")
            self.class_weight_label.setText(f"{state.class_weight.get():.2f}")
            
            # 更新时间
            from datetime import datetime
            self.update_time_label.setText(f"更新时间: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"更新状态失败: {e}")
            
    def stop_timer(self):
        """停止定时器"""
        if hasattr(self, 'timer'):
            self.timer.stop()


def create_target_selector_state():
    """
    创建目标选择器状态显示组件
    
    Returns:
        TargetSelectorStateWidget: 目标选择器状态显示组件
    """
    return TargetSelectorStateWidget()


if __name__ == "__main__":
    # 测试组件
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = create_target_selector_state()
    widget.show()
    
    sys.exit(app.exec())
