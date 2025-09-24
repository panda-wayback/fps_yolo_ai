#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID控制器组件主入口
整合配置、状态和测试组件
"""

import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout

from pyside.UI.basic.basic_layout import create_vertical_card
from pyside.UI.basic.basic_window import create_scrollable_window
from pyside.fps_ai_ui.component.pid_controller.component.pid_config import create_pid_config
from pyside.fps_ai_ui.component.pid_controller.component.pid_state import create_pid_state


def get_pid_config_component():
    """ 
    创建PID控制器配置组件
    
    Returns:
        PIDConfigWidget: PID控制器配置组件
    """
    return create_pid_config()


def get_pid_state_component():
    """
    创建PID控制器状态显示组件
    
    Returns:
        PIDStateWidget: PID控制器状态显示组件
    """
    return create_pid_state()


def get_pid_controller_component():
    """
    创建完整的PID控制器组件
    
    Returns:
        QGroupBox: 完整的PID控制器组件
    """
    # 创建主容器
    group = create_vertical_card("PID控制器")
    main_layout = group._layout
    
    # 上半部分：配置和状态
    top_layout = QHBoxLayout()
    
    # 配置组件
    config_widget = get_pid_config_component()
    config_widget.setMinimumWidth(300)
    top_layout.addWidget(config_widget)
    
    # 状态显示组件
    state_widget = get_pid_state_component()
    state_widget.setMinimumWidth(250)
    top_layout.addWidget(state_widget)
    
    main_layout.addLayout(top_layout)
    
    return group


if __name__ == "__main__":
    # 测试PID控制器组件
    app = QApplication(sys.argv)
    window = create_scrollable_window()
    
    # 创建PID控制器组件
    pid_controller_group = get_pid_controller_component()
    
    # 检查content_widget是否已有布局
    if window.content_widget.layout() is None:
        from PySide6.QtWidgets import QVBoxLayout
        window.content_widget.setLayout(QVBoxLayout())
    
    window.content_widget.layout().addWidget(pid_controller_group)
    
    window.show()
    sys.exit(app.exec())
