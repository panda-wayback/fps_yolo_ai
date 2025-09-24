"""
02. 添加按钮
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("带按钮的窗口")
window.resize(400, 300)

# 创建按钮
button = QPushButton("点击我", window)
button.move(150, 100)

window.show()
sys.exit(app.exec())
