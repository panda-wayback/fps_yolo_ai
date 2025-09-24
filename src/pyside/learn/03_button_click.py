"""
03. 按钮点击事件
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("按钮点击事件")
window.resize(400, 300)

# 创建按钮
button = QPushButton("点击我", window)
button.move(150, 100)

# 按钮点击事件
def on_click():
    print("按钮被点击了!")

button.clicked.connect(on_click)

window.show()
sys.exit(app.exec())
