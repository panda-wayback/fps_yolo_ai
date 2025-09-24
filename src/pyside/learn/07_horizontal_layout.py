"""
08. 水平布局 - 组件左右排列
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("水平布局 - 左右排列")
window.resize(400, 300)

# 创建水平布局
layout = QHBoxLayout()

# 创建组件
label = QLabel("第一个")
button1 = QPushButton("第二个")
button2 = QPushButton("第三个")

# 按顺序添加到布局（从左到右）
layout.addWidget(label)
layout.addWidget(button1)
layout.addWidget(button2)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
