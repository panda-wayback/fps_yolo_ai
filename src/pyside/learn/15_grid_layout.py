"""
15. 网格布局示例
展示 QGridLayout 网格布局的使用
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("网格布局示例")
window.resize(400, 300)

# 创建网格布局
layout = QGridLayout()

# 添加组件到网格中
# 格式：layout.addWidget(组件, 行, 列)
layout.addWidget(QLabel("(0,0)"), 0, 0)
layout.addWidget(QLabel("(0,1)"), 0, 1)
layout.addWidget(QLabel("(0,2)"), 0, 2)

layout.addWidget(QLabel("(1,0)"), 1, 0)
layout.addWidget(QLabel("(1,1)"), 1, 1)
layout.addWidget(QLabel("(1,2)"), 1, 2)

layout.addWidget(QLabel("(2,0)"), 2, 0)
layout.addWidget(QLabel("(2,1)"), 2, 1)
layout.addWidget(QLabel("(2,2)"), 2, 2)

# 设置布局
window.setLayout(layout)

window.show()
sys.exit(app.exec())
