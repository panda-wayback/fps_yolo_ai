"""
09. 混合布局 - 垂直+水平
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("混合布局")
window.resize(400, 300)

# 主布局（垂直）
main_layout = QVBoxLayout()

# 第一行（水平布局）
row1 = QHBoxLayout()
row1.addWidget(QLabel("左"))
row1.addWidget(QPushButton("中"))
row1.addWidget(QLabel("右"))

# 第二行（水平布局）
row2 = QHBoxLayout()
row2.addWidget(QPushButton("按钮1"))
row2.addWidget(QPushButton("按钮2"))

# 添加到主布局
main_layout.addLayout(row1)
main_layout.addLayout(row2)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
