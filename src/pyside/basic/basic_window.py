"""
基本窗口组件 - 简单函数实现
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


def create_basic_window(title="基础窗口", width=400, height=300):
    window = QWidget()
    window.setWindowTitle(title)
    window.resize(width, height)
    return window


def main():
    app = QApplication(sys.argv)
    window = create_basic_window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
