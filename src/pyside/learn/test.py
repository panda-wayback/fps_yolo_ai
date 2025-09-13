from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
import sys

app = QApplication(sys.argv)

window = QWidget()
layout = QHBoxLayout()

layout.addWidget(QPushButton("Left"))
layout.addWidget(QPushButton("Center"))
layout.addWidget(QPushButton("Right"))

window.setLayout(layout)
window.show()
sys.exit(app.exec())
