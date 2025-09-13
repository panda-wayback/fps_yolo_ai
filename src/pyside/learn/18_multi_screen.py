"""
18. 多屏幕显示示例
展示如何在指定屏幕显示窗口
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

# 获取屏幕信息
screens = app.screens()
print(f"检测到 {len(screens)} 个屏幕")

for i, screen in enumerate(screens):
    print(f"屏幕 {i}: {screen.name()}, 分辨率: {screen.size().width()}x{screen.size().height()}")

window = QWidget()
window.setWindowTitle("多屏幕显示示例")
window.resize(400, 300)

# 创建布局
layout = QVBoxLayout()
window.setLayout(layout)

# 添加标签显示当前屏幕信息
current_screen = window.screen()
info_label = QLabel(f"当前屏幕: {current_screen.name()}\n分辨率: {current_screen.size().width()}x{current_screen.size().height()}")
info_label.setAlignment(Qt.AlignCenter)
layout.addWidget(info_label)

# 添加按钮
btn1 = QPushButton("显示在屏幕1")
btn2 = QPushButton("显示在屏幕2")
btn3 = QPushButton("显示在屏幕3")

layout.addWidget(btn1)
layout.addWidget(btn2)
layout.addWidget(btn3)

# 按钮事件
def show_on_screen(screen_index):
    """在指定屏幕显示窗口"""
    if screen_index < len(screens):
        screen = screens[screen_index]
        # 移动到指定屏幕
        window.move(screen.geometry().x(), screen.geometry().y())
        # 或者使用 setScreen
        # window.setScreen(screen)
        print(f"窗口移动到屏幕 {screen_index}: {screen.name()}")

btn1.clicked.connect(lambda: show_on_screen(0))
btn2.clicked.connect(lambda: show_on_screen(1))
btn3.clicked.connect(lambda: show_on_screen(2))

window.show()
sys.exit(app.exec())
