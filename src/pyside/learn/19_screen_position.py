"""
19. 屏幕位置控制示例
展示如何控制窗口在屏幕上的位置
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("屏幕位置控制示例")
window.resize(400, 300)

# 创建布局
layout = QVBoxLayout()
window.setLayout(layout)

# 添加标签
info_label = QLabel("点击按钮控制窗口位置")
info_label.setAlignment(Qt.AlignCenter)
layout.addWidget(info_label)

# 添加按钮
btn1 = QPushButton("显示在屏幕1")
btn2 = QPushButton("显示在屏幕2")
btn3 = QPushButton("居中显示")
btn4 = QPushButton("左上角")
btn5 = QPushButton("右下角")

layout.addWidget(btn1)
layout.addWidget(btn2)
layout.addWidget(btn3)
layout.addWidget(btn4)
layout.addWidget(btn5)

# 获取屏幕信息
screens = app.screens()

def show_on_screen1():
    """显示在屏幕1"""
    if len(screens) > 0:
        screen = screens[0]
        window.move(screen.geometry().x(), screen.geometry().y())
        print(f"移动到屏幕1: {screen.name()}")

def show_on_screen2():
    """显示在屏幕2"""
    if len(screens) > 1:
        screen = screens[1]
        window.move(screen.geometry().x(), screen.geometry().y())
        print(f"移动到屏幕2: {screen.name()}")

def center_window():
    """居中显示"""
    screen = window.screen()
    screen_geometry = screen.geometry()
    window_geometry = window.geometry()
    
    x = screen_geometry.x() + (screen_geometry.width() - window_geometry.width()) // 2
    y = screen_geometry.y() + (screen_geometry.height() - window_geometry.height()) // 2
    
    window.move(x, y)
    print(f"窗口居中显示在: {screen.name()}")

def top_left():
    """左上角"""
    screen = window.screen()
    window.move(screen.geometry().x(), screen.geometry().y())
    print("窗口移动到左上角")

def bottom_right():
    """右下角"""
    screen = window.screen()
    screen_geometry = screen.geometry()
    window_geometry = window.geometry()
    
    x = screen_geometry.x() + screen_geometry.width() - window_geometry.width()
    y = screen_geometry.y() + screen_geometry.height() - window_geometry.height()
    
    window.move(x, y)
    print("窗口移动到右下角")

# 连接按钮事件
btn1.clicked.connect(show_on_screen1)
btn2.clicked.connect(show_on_screen2)
btn3.clicked.connect(center_window)
btn4.clicked.connect(top_left)
btn5.clicked.connect(bottom_right)

window.show()
sys.exit(app.exec())
