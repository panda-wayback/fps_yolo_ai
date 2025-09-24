"""
14. 高级控件示例
展示更复杂的输入控件：日期选择、颜色选择、文件选择等
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QLineEdit, QDateEdit, 
                               QTimeEdit, QDateTimeEdit, QColorDialog, 
                               QFileDialog, QFontDialog, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt, QDate, QTime, QDateTime
from PySide6.QtGui import QFont

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("高级控件示例")
window.resize(600, 700)

# 主布局
main_layout = QVBoxLayout()

# 1. 日期时间组
datetime_group = QGroupBox("日期时间选择")
datetime_layout = QVBoxLayout()

# 日期选择
datetime_layout.addWidget(QLabel("日期选择:"))
date_edit = QDateEdit()
date_edit.setDate(QDate.currentDate())  # 设置当前日期
date_edit.setCalendarPopup(True)        # 显示日历弹窗
datetime_layout.addWidget(date_edit)

# 时间选择
datetime_layout.addWidget(QLabel("时间选择:"))
time_edit = QTimeEdit()
time_edit.setTime(QTime.currentTime())  # 设置当前时间
datetime_layout.addWidget(time_edit)

# 日期时间选择
datetime_layout.addWidget(QLabel("日期时间选择:"))
datetime_edit = QDateTimeEdit()
datetime_edit.setDateTime(QDateTime.currentDateTime())  # 设置当前日期时间
datetime_layout.addWidget(datetime_edit)

datetime_group.setLayout(datetime_layout)
main_layout.addWidget(datetime_group)

# 2. 颜色选择组
color_group = QGroupBox("颜色选择")
color_layout = QVBoxLayout()

# 颜色选择按钮
color_btn = QPushButton("选择颜色")
color_preview = QLabel("颜色预览")
color_preview.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
color_preview.setAlignment(Qt.AlignCenter)

color_layout.addWidget(QLabel("点击按钮选择颜色:"))
color_layout.addWidget(color_btn)
color_layout.addWidget(color_preview)

color_group.setLayout(color_layout)
main_layout.addWidget(color_group)

# 3. 文件选择组
file_group = QGroupBox("文件选择")
file_layout = QVBoxLayout()

# 文件选择按钮
file_btn = QPushButton("选择文件")
file_path = QLineEdit()
file_path.setPlaceholderText("选择的文件路径将显示在这里...")
file_path.setReadOnly(True)  # 只读

# 文件夹选择按钮
folder_btn = QPushButton("选择文件夹")
folder_path = QLineEdit()
folder_path.setPlaceholderText("选择的文件夹路径将显示在这里...")
folder_path.setReadOnly(True)

file_layout.addWidget(QLabel("文件选择:"))
file_layout.addWidget(file_btn)
file_layout.addWidget(file_path)
file_layout.addWidget(QLabel("文件夹选择:"))
file_layout.addWidget(folder_btn)
file_layout.addWidget(folder_path)

file_group.setLayout(file_layout)
main_layout.addWidget(file_group)

# 4. 字体选择组
font_group = QGroupBox("字体选择")
font_layout = QVBoxLayout()

# 字体选择按钮
font_btn = QPushButton("选择字体")
font_preview = QLabel("字体预览文本")
font_preview.setStyleSheet("padding: 10px; border: 1px solid #bdc3c7;")
font_preview.setAlignment(Qt.AlignCenter)

font_layout.addWidget(QLabel("点击按钮选择字体:"))
font_layout.addWidget(font_btn)
font_layout.addWidget(font_preview)

font_group.setLayout(font_layout)
main_layout.addWidget(font_group)

# 5. 多行文本组
text_group = QGroupBox("多行文本编辑")
text_layout = QVBoxLayout()

# 多行文本编辑器
text_edit = QTextEdit()
text_edit.setPlaceholderText("在这里输入多行文本...")
text_edit.setMaximumHeight(150)
text_layout.addWidget(text_edit)

# 文本操作按钮
text_btn_layout = QHBoxLayout()
clear_text_btn = QPushButton("清空文本")
get_text_btn = QPushButton("获取文本")
text_btn_layout.addWidget(clear_text_btn)
text_btn_layout.addWidget(get_text_btn)
text_layout.addLayout(text_btn_layout)

text_group.setLayout(text_layout)
main_layout.addWidget(text_group)

# 6. 结果显示组
result_group = QGroupBox("结果显示")
result_layout = QVBoxLayout()

# 结果显示区域
result_text = QTextEdit()
result_text.setReadOnly(True)
result_text.setMaximumHeight(100)
result_text.setPlaceholderText("选择的值将显示在这里...")
result_layout.addWidget(result_text)

result_group.setLayout(result_layout)
main_layout.addWidget(result_group)

# 7. 按钮组
button_layout = QHBoxLayout()
get_all_btn = QPushButton("获取所有值")
clear_all_btn = QPushButton("清空所有")
button_layout.addWidget(get_all_btn)
button_layout.addWidget(clear_all_btn)
main_layout.addLayout(button_layout)

# 事件处理函数
def choose_color():
    """选择颜色"""
    color = QColorDialog.getColor()
    if color.isValid():
        color_preview.setStyleSheet(f"background-color: {color.name()}; color: white; padding: 10px;")
        result_text.append(f"选择的颜色: {color.name()}")

def choose_file():
    """选择文件"""
    file_path_text, _ = QFileDialog.getOpenFileName(
        window, 
        "选择文件", 
        "", 
        "所有文件 (*);;文本文件 (*.txt);;Python文件 (*.py)"
    )
    if file_path_text:
        file_path.setText(file_path_text)
        result_text.append(f"选择的文件: {file_path_text}")

def choose_folder():
    """选择文件夹"""
    folder_path_text = QFileDialog.getExistingDirectory(window, "选择文件夹")
    if folder_path_text:
        folder_path.setText(folder_path_text)
        result_text.append(f"选择的文件夹: {folder_path_text}")

def choose_font():
    """选择字体"""
    font, ok = QFontDialog.getFont()
    if ok:
        font_preview.setFont(font)
        result_text.append(f"选择的字体: {font.family()}, 大小: {font.pointSize()}")

def clear_text():
    """清空文本"""
    text_edit.clear()

def get_text():
    """获取文本"""
    text = text_edit.toPlainText()
    result_text.append(f"文本内容: {text}")

def get_all_values():
    """获取所有值"""
    result_text.clear()
    result_text.append("=== 所有选择的值 ===")
    result_text.append(f"日期: {date_edit.date().toString()}")
    result_text.append(f"时间: {time_edit.time().toString()}")
    result_text.append(f"日期时间: {datetime_edit.dateTime().toString()}")
    result_text.append(f"文件: {file_path.text()}")
    result_text.append(f"文件夹: {folder_path.text()}")
    result_text.append(f"文本: {text_edit.toPlainText()}")

def clear_all():
    """清空所有"""
    date_edit.setDate(QDate.currentDate())
    time_edit.setTime(QTime.currentTime())
    datetime_edit.setDateTime(QDateTime.currentDateTime())
    file_path.clear()
    folder_path.clear()
    text_edit.clear()
    result_text.clear()
    color_preview.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
    font_preview.setFont(QFont())

# 连接信号和槽
color_btn.clicked.connect(choose_color)
file_btn.clicked.connect(choose_file)
folder_btn.clicked.connect(choose_folder)
font_btn.clicked.connect(choose_font)
clear_text_btn.clicked.connect(clear_text)
get_text_btn.clicked.connect(get_text)
get_all_btn.clicked.connect(get_all_values)
clear_all_btn.clicked.connect(clear_all)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
