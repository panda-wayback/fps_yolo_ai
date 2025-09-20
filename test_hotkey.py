#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试快捷键功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pyside.fps_ai_ui.component.screenshot import get_screenshot_component
from PySide6.QtWidgets import QApplication
from pyside.UI.basic.basic_window import create_scrollable_window

def test_hotkey():
    """测试快捷键功能"""
    app = QApplication(sys.argv)
    window = create_scrollable_window()
    
    # 创建截图组件
    screenshot_component = get_screenshot_component()
    
    # 检查 content_widget 是否已有布局
    if window.content_widget.layout() is None:
        from PySide6.QtWidgets import QVBoxLayout
        window.content_widget.setLayout(QVBoxLayout())
    
    window.content_widget.layout().addWidget(screenshot_component)
    window.show()
    
    print("✅ 快捷键测试启动")
    print("📝 使用说明:")
    print("   - 按 Ctrl+M 获取鼠标位置")
    print("   - 点击 '获取鼠标位置' 按钮也可以")
    print("   - 关闭窗口退出测试")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_hotkey()
