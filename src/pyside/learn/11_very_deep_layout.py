"""
11. 超深层布局 - 5层嵌套示例
展示布局可以有多深，就像俄罗斯套娃
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
                               QVBoxLayout, QHBoxLayout, QGroupBox)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("超深层布局 - 5层嵌套")
window.resize(800, 600)

# 第1层：主窗口布局（垂直）
main = QVBoxLayout()

# 第2层：头部区域（水平）
header = QHBoxLayout()

# 第3层：头部左侧（垂直）
header_left = QVBoxLayout()
header_left.addWidget(QLabel("头部左侧"))

# 第4层：头部左侧按钮组（水平）
header_left_buttons = QHBoxLayout()
header_left_buttons.addWidget(QPushButton("头左1"))
header_left_buttons.addWidget(QPushButton("头左2"))

header_left.addLayout(header_left_buttons)

# 第3层：头部中间（垂直）
header_center = QVBoxLayout()
header_center.addWidget(QLabel("头部中间"))

# 第4层：头部中间按钮组（水平）
header_center_buttons = QHBoxLayout()
header_center_buttons.addWidget(QPushButton("头中1"))
header_center_buttons.addWidget(QPushButton("头中2"))
header_center_buttons.addWidget(QPushButton("头中3"))

header_center.addLayout(header_center_buttons)

# 第3层：头部右侧（垂直）
header_right = QVBoxLayout()
header_right.addWidget(QLabel("头部右侧"))
header_right.addWidget(QPushButton("头右按钮"))

# 将第3层添加到第2层
header.addLayout(header_left)
header.addLayout(header_center)
header.addLayout(header_right)

# 第2层：内容区域（水平）
content = QHBoxLayout()

# 第3层：侧边栏（垂直）
sidebar = QVBoxLayout()
sidebar.addWidget(QLabel("侧边栏"))

# 第4层：侧边栏按钮组（垂直）
sidebar_buttons = QVBoxLayout()
sidebar_buttons.addWidget(QPushButton("侧1"))
sidebar_buttons.addWidget(QPushButton("侧2"))
sidebar_buttons.addWidget(QPushButton("侧3"))

sidebar.addLayout(sidebar_buttons)

# 第3层：主内容区（垂直）
main_content = QVBoxLayout()
main_content.addWidget(QLabel("主内容区"))

# 第4层：主内容按钮组（水平）
main_buttons = QHBoxLayout()
main_buttons.addWidget(QPushButton("主1"))
main_buttons.addWidget(QPushButton("主2"))

main_content.addLayout(main_buttons)

# 第4层：主内容文本区（水平）
main_text = QHBoxLayout()
main_text.addWidget(QLabel("文本1"))
main_text.addWidget(QLabel("文本2"))

main_content.addLayout(main_text)

# 第3层：右侧面板（垂直）
right_panel = QVBoxLayout()
right_panel.addWidget(QLabel("右侧面板"))

# 第4层：右侧按钮组（水平）
right_buttons = QHBoxLayout()
right_buttons.addWidget(QPushButton("右1"))
right_buttons.addWidget(QPushButton("右2"))

right_panel.addLayout(right_buttons)

# 第4层：右侧文本组（水平）
right_text = QHBoxLayout()
right_text.addWidget(QLabel("右文本1"))
right_text.addWidget(QLabel("右文本2"))

right_panel.addLayout(right_text)

# 将第3层添加到第2层
content.addLayout(sidebar)
content.addLayout(main_content)
content.addLayout(right_panel)

# 第2层：底部区域（水平）
footer = QHBoxLayout()

# 第3层：底部左侧（垂直）
footer_left = QVBoxLayout()
footer_left.addWidget(QLabel("底部左侧"))

# 第4层：底部左侧按钮组（水平）
footer_left_buttons = QHBoxLayout()
footer_left_buttons.addWidget(QPushButton("底左1"))
footer_left_buttons.addWidget(QPushButton("底左2"))

footer_left.addLayout(footer_left_buttons)

# 第3层：底部中间（垂直）
footer_center = QVBoxLayout()
footer_center.addWidget(QLabel("底部中间"))

# 第4层：底部中间按钮组（水平）
footer_center_buttons = QHBoxLayout()
footer_center_buttons.addWidget(QPushButton("底中1"))
footer_center_buttons.addWidget(QPushButton("底中2"))
footer_center_buttons.addWidget(QPushButton("底中3"))

footer_center.addLayout(footer_center_buttons)

# 第3层：底部右侧（垂直）
footer_right = QVBoxLayout()
footer_right.addWidget(QLabel("底部右侧"))

# 第4层：底部右侧按钮组（水平）
footer_right_buttons = QHBoxLayout()
footer_right_buttons.addWidget(QPushButton("底右1"))
footer_right_buttons.addWidget(QPushButton("底右2"))

footer_right.addLayout(footer_right_buttons)

# 将第3层添加到第2层
footer.addLayout(footer_left)
footer.addLayout(footer_center)
footer.addLayout(footer_right)

# 将第2层添加到第1层
main.addLayout(header)
main.addLayout(content)
main.addLayout(footer)

# 设置主布局
window.setLayout(main)
window.show()
sys.exit(app.exec())
