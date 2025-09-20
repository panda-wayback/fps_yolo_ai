#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标驱动组件主入口
整合配置、状态和测试组件
"""

import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout

from pyside.UI.basic.basic_layout import create_vertical_card
from pyside.UI.basic.basic_window import create_scrollable_window
from pyside.fps_ai_ui.component.mouse_driver.component.mouse_driver_config import create_mouse_driver_config
from pyside.fps_ai_ui.component.mouse_driver.component.mouse_driver_state import create_mouse_driver_state

def get_mouse_driver_config_component():
    """ 
    创建鼠标驱动配置组件
    
    Returns:
        MouseDriverConfigWidget: 鼠标驱动配置组件
    """
    return create_mouse_driver_config()


def get_mouse_driver_state_component():
    """
    创建鼠标驱动状态显示组件
    
    Returns:
        MouseDriverStateWidget: 鼠标驱动状态显示组件
    """
    return create_mouse_driver_state()




def get_mouse_driver_component():
    """
    创建完整的鼠标驱动组件
    
    Returns:
        QGroupBox: 完整的鼠标驱动组件
    """
    # 创建主容器
    group = create_vertical_card("鼠标驱动控制器")
    main_layout = group._layout
    
    # 上半部分：配置和状态
    top_layout = QHBoxLayout()
    
    # 配置组件
    config_widget = get_mouse_driver_config_component()
    config_widget.setMinimumWidth(300)
    top_layout.addWidget(config_widget)
    
    # 状态显示组件
    state_widget = get_mouse_driver_state_component()
    state_widget.setMinimumWidth(250)
    top_layout.addWidget(state_widget)
    
    main_layout.addLayout(top_layout)
    

    
    return group


if __name__ == "__main__":
    # 测试鼠标驱动组件
    app = QApplication(sys.argv)
    window = create_scrollable_window()
    
    # 创建鼠标驱动组件
    mouse_driver_group = get_mouse_driver_component()
    
    # 检查content_widget是否已有布局
    if window.content_widget.layout() is None:
        from PySide6.QtWidgets import QVBoxLayout
        window.content_widget.setLayout(QVBoxLayout())
    
    window.content_widget.layout().addWidget(mouse_driver_group)
    
    window.show()
    sys.exit(app.exec())
