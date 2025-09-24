"""
01. 最简单的窗口
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("我的第一个窗口")
window.resize(400, 300)
window.show()

sys.exit(app.exec())
