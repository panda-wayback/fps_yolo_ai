"""
07. 垂直布局 - 组件上下排列
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("垂直布局 - 上下排列")
window.resize(400, 300)

# 创建垂直布局
layout = QVBoxLayout()

# 创建组件
label = QLabel("第一个组件")
button1 = QPushButton("第二个组件")
button2 = QPushButton("第三个组件")

# 按顺序添加到布局（从上到下）
layout.addWidget(label)
layout.addWidget(button1)
layout.addWidget(button2)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
