"""
10. 深层布局 - 多层嵌套布局示例
展示布局可以有多深的层次
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
                               QVBoxLayout, QHBoxLayout, QGroupBox)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("深层布局 - 多层嵌套")
window.resize(600, 500)

# 第1层：主布局（垂直）
main_layout = QVBoxLayout()

# 第2层：顶部区域（水平布局）
top_area = QHBoxLayout()

# 第3层：左侧面板（垂直布局）
left_panel = QVBoxLayout()
left_panel.addWidget(QLabel("左侧标题"))
left_panel.addWidget(QPushButton("左按钮1"))
left_panel.addWidget(QPushButton("左按钮2"))

# 第3层：中间面板（垂直布局）
middle_panel = QVBoxLayout()
middle_panel.addWidget(QLabel("中间标题"))

# 第4层：中间按钮组（水平布局）
middle_buttons = QHBoxLayout()
middle_buttons.addWidget(QPushButton("中1"))
middle_buttons.addWidget(QPushButton("中2"))
middle_buttons.addWidget(QPushButton("中3"))

middle_panel.addLayout(middle_buttons)  # 将第4层添加到第3层

# 第3层：右侧面板（垂直布局）
right_panel = QVBoxLayout()
right_panel.addWidget(QLabel("右侧标题"))

# 第4层：右侧按钮组（水平布局）
right_buttons = QHBoxLayout()
right_buttons.addWidget(QPushButton("右1"))
right_buttons.addWidget(QPushButton("右2"))

right_panel.addLayout(right_buttons)  # 将第4层添加到第3层

# 将第3层添加到第2层
top_area.addLayout(left_panel)
top_area.addLayout(middle_panel)
top_area.addLayout(right_panel)

# 第2层：底部区域（水平布局）
bottom_area = QHBoxLayout()

# 第3层：底部左侧（垂直布局）
bottom_left = QVBoxLayout()
bottom_left.addWidget(QLabel("底部左侧"))

# 第4层：底部左侧按钮组（水平布局）
bottom_left_buttons = QHBoxLayout()
bottom_left_buttons.addWidget(QPushButton("底左1"))
bottom_left_buttons.addWidget(QPushButton("底左2"))
bottom_left_buttons.addWidget(QPushButton("底左3"))

bottom_left.addLayout(bottom_left_buttons)

# 第3层：底部右侧（垂直布局）
bottom_right = QVBoxLayout()
bottom_right.addWidget(QLabel("底部右侧"))
bottom_right.addWidget(QPushButton("底右按钮"))

# 将第3层添加到第2层
bottom_area.addLayout(bottom_left)
bottom_area.addLayout(bottom_right)

# 将第2层添加到第1层
main_layout.addLayout(top_area)
main_layout.addLayout(bottom_area)

# 设置主布局
window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
