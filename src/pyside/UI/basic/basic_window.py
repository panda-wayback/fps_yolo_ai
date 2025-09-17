"""
基本窗口组件 - 简单函数实现
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame)
from PySide6.QtCore import Qt


def create_basic_window(title="基础窗口", width=400, height=300):
    window = QWidget()
    window.setWindowTitle(title)
    window.resize(width, height)
    return window


def create_scrollable_window(title="FPS AI 控制台", width=1200, height=800):
    """
    创建可滚动的窗口，适合显示大量组件
    
    Args:
        title: 窗口标题
        width: 窗口宽度
        height: 窗口高度
        
    Returns:
        QWidget: 可滚动的窗口
    """
    window = QWidget()
    window.setWindowTitle(title)
    window.resize(width, height)
    
    # 创建滚动区域
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
    # 创建内容容器
    content_widget = QFrame()
    content_widget.setFrameStyle(QFrame.NoFrame)
    
    # 设置滚动区域的内容
    scroll_area.setWidget(content_widget)
    
    # 创建主布局
    main_layout = QVBoxLayout()
    main_layout.addWidget(scroll_area)
    main_layout.setContentsMargins(0, 0, 0, 0)
    
    window.setLayout(main_layout)
    
    # 存储内容容器的引用，方便后续添加组件
    window.content_widget = content_widget
    
    return window


def main():
    app = QApplication(sys.argv)
    window = create_basic_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
