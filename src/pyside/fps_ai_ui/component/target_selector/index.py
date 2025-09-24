#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器组件主入口
整合配置和状态显示组件
"""

from PySide6.QtWidgets import QVBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt

from pyside.fps_ai_ui.component.target_selector.component.target_selector_config import create_target_selector_config
from pyside.fps_ai_ui.component.target_selector.component.target_selector_state import create_target_selector_state



def create_target_selector_component():
    """
    创建目标选择器组件
    
    Returns:
        QWidget: 目标选择器组件
    """
    # 创建主容器
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # 创建分割器
    splitter = QSplitter(Qt.Horizontal)
    
    # 创建配置组件
    config_widget = create_target_selector_config()
    splitter.addWidget(config_widget)
    
    # 创建状态显示组件
    state_widget = create_target_selector_state()
    splitter.addWidget(state_widget)
    
    # 设置分割器比例
    splitter.setSizes([400, 300])
    
    layout.addWidget(splitter)
    
    return widget

def get_target_selector_component():
    return create_target_selector_component()

if __name__ == "__main__":
    # 测试组件
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = create_target_selector_component()
    widget.show()
    
    sys.exit(app.exec())
