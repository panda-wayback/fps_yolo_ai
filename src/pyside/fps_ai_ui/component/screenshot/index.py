#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图组件索引
"""

import sys
from PySide6.QtWidgets import QApplication

from pyside.UI.basic.basic_window import create_scrollable_window
from pyside.fps_ai_ui.component.screenshot.component.screenshot_config import get_screenshot_config


def get_screenshot_config_component():
    """
    创建截图设置组件
    
    Returns:
        QGroupBox: 截图设置组件
    """
    return get_screenshot_config()


def get_screenshot_component():
    """
    创建截图组件集合
    
    Returns:
        QGroupBox: 截图组件集合
    """
    from pyside.UI.basic.basic_layout import create_vertical_card
    
    group = create_vertical_card("截图功能")
    group._layout.addWidget(get_screenshot_config_component())
     
    return group

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_scrollable_window()
    if window.content_widget.layout() is None:
        from PySide6.QtWidgets import QVBoxLayout
        window.content_widget.setLayout(QVBoxLayout())
    window.content_widget.layout().addWidget(get_screenshot_component())
    window.show()
    sys.exit(app.exec())