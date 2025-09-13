import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout

from pyside.basic.basic_window import create_basic_window


# 获取垂直布局
def get_vertical_layout():
    return QVBoxLayout()

# 获取水平布局
def get_horizontal_layout():
    return QHBoxLayout()

# 获取网格布局
def get_grid_layout():
    return QGridLayout()


def main():
    app = QApplication(sys.argv)
    window = create_basic_window()
    layout = get_vertical_layout()
    layout.addWidget(QLabel("Hello, World!"))
    # 设置布局
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()