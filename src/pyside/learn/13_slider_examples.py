"""
13. 拖动参数示例
展示各种拖动控件：滑块、进度条、范围滑块等
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QSlider, QProgressBar, 
                               QGroupBox, QSpinBox, QDoubleSpinBox)
from PySide6.QtCore import QTimer, Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("拖动参数示例")
window.resize(500, 600)

# 主布局
main_layout = QVBoxLayout()

# 1. 基础滑块组
slider_group = QGroupBox("基础滑块")
slider_layout = QVBoxLayout()

# 水平滑块
slider_layout.addWidget(QLabel("水平滑块:"))
h_slider = QSlider(Qt.Horizontal)
h_slider.setRange(0, 100)      # 设置范围 0-100
h_slider.setValue(50)          # 设置默认值
h_slider.setTickPosition(QSlider.TicksBelow)  # 显示刻度
h_slider.setTickInterval(10)   # 刻度间隔
slider_layout.addWidget(h_slider)

# 垂直滑块
slider_layout.addWidget(QLabel("垂直滑块:"))
v_slider = QSlider(Qt.Vertical)
v_slider.setRange(0, 100)
v_slider.setValue(30)
v_slider.setTickPosition(QSlider.TicksLeft)
v_slider.setTickInterval(20)
slider_layout.addWidget(v_slider)

slider_group.setLayout(slider_layout)
main_layout.addWidget(slider_group)

# 2. 滑块与数字联动组
sync_group = QGroupBox("滑块与数字联动")
sync_layout = QVBoxLayout()

# 创建滑块和数字输入框
sync_slider = QSlider(Qt.Horizontal)
sync_slider.setRange(0, 100)
sync_slider.setValue(25)

sync_spin = QSpinBox()
sync_spin.setRange(0, 100)
sync_spin.setValue(25)

# 滑块值改变时，更新数字框
def on_slider_changed(value):
    sync_spin.setValue(value)

# 数字框值改变时，更新滑块
def on_spin_changed(value):
    sync_slider.setValue(value)

sync_slider.valueChanged.connect(on_slider_changed)
sync_spin.valueChanged.connect(on_spin_changed)

sync_layout.addWidget(QLabel("拖动滑块或输入数字:"))
sync_layout.addWidget(sync_slider)
sync_layout.addWidget(sync_spin)

sync_group.setLayout(sync_layout)
main_layout.addWidget(sync_group)

# 3. 进度条组
progress_group = QGroupBox("进度条")
progress_layout = QVBoxLayout()

# 进度条
progress_bar = QProgressBar()
progress_bar.setRange(0, 100)
progress_bar.setValue(0)
progress_layout.addWidget(QLabel("进度条:"))
progress_layout.addWidget(progress_bar)

# 控制按钮
progress_btn_layout = QHBoxLayout()
timer = QTimer()
timer.timeout.connect(lambda: progress_bar.setValue(progress_bar.value() + 1))
start_btn = QPushButton("开始", 
    clicked = lambda: timer.start(300)
    )
pause_btn = QPushButton("暂停",
    clicked = lambda: timer.stop()
    )
reset_btn = QPushButton("重置",
    clicked = lambda: progress_bar.setValue(0)
    )
progress_btn_layout.addWidget(start_btn)
progress_btn_layout.addWidget(pause_btn)
progress_btn_layout.addWidget(reset_btn)
progress_layout.addLayout(progress_btn_layout)

progress_group.setLayout(progress_layout)
main_layout.addWidget(progress_group)

# 4. 多滑块控制组
multi_group = QGroupBox("多滑块控制")
multi_layout = QVBoxLayout()

# 音量控制
volume_layout = QHBoxLayout()
volume_layout.addWidget(QLabel("音量:"))
volume_slider = QSlider(Qt.Horizontal)
volume_slider.setRange(0, 100)
volume_slider.setValue(80)
volume_label = QLabel("80%")
volume_layout.addWidget(volume_slider)
volume_layout.addWidget(volume_label)
multi_layout.addLayout(volume_layout)

# 亮度控制
brightness_layout = QHBoxLayout()
brightness_layout.addWidget(QLabel("亮度:"))
brightness_slider = QSlider(Qt.Horizontal)
brightness_slider.setRange(0, 100)
brightness_slider.setValue(60)
brightness_label = QLabel("60%")
brightness_layout.addWidget(brightness_slider)
brightness_layout.addWidget(brightness_label)
multi_layout.addLayout(brightness_layout)

# 对比度控制
contrast_layout = QHBoxLayout()
contrast_layout.addWidget(QLabel("对比度:"))
contrast_slider = QSlider(Qt.Horizontal)
contrast_slider.setRange(0, 100)
contrast_slider.setValue(70)
contrast_label = QLabel("70%")
contrast_layout.addWidget(contrast_slider)
contrast_layout.addWidget(contrast_label)
multi_layout.addLayout(contrast_layout)

multi_group.setLayout(multi_layout)
main_layout.addWidget(multi_group)

# 5. 实时显示组
display_group = QGroupBox("实时显示")
display_layout = QVBoxLayout()

# 显示标签
display_label = QLabel("当前值: 0")
display_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
display_layout.addWidget(display_label)

# 控制滑块
display_slider = QSlider(Qt.Horizontal)
display_slider.setRange(0, 100)
display_slider.setValue(0)

# 滑块值改变时更新显示
def update_display(value):
    display_label.setText(f"当前值: {value}")
    # 根据值改变颜色
    if value < 30:
        color = "#e74c3c"  # 红色
    elif value < 70:
        color = "#f39c12"  # 橙色
    else:
        color = "#27ae60"  # 绿色
    
    display_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")

display_slider.valueChanged.connect(update_display)
display_layout.addWidget(display_slider)

display_group.setLayout(display_layout)
main_layout.addWidget(display_group)

# 6. 按钮组
button_layout = QHBoxLayout()
get_values_btn = QPushButton("获取所有值")
reset_all_btn = QPushButton("重置所有")
button_layout.addWidget(get_values_btn)
button_layout.addWidget(reset_all_btn)
main_layout.addLayout(button_layout)

# 按钮事件
def get_all_values():
    """获取所有滑块值"""
    print("=== 所有滑块值 ===")
    print(f"水平滑块: {h_slider.value()}")
    print(f"垂直滑块: {v_slider.value()}")
    print(f"联动滑块: {sync_slider.value()}")
    print(f"音量: {volume_slider.value()}%")
    print(f"亮度: {brightness_slider.value()}%")
    print(f"对比度: {contrast_slider.value()}%")
    print(f"显示滑块: {display_slider.value()}")

def reset_all():
    """重置所有滑块"""
    h_slider.setValue(0)
    v_slider.setValue(0)
    sync_slider.setValue(0)
    sync_spin.setValue(0)
    volume_slider.setValue(0)
    brightness_slider.setValue(0)
    contrast_slider.setValue(0)
    display_slider.setValue(0)
    progress_bar.setValue(0)

get_values_btn.clicked.connect(get_all_values)
reset_all_btn.clicked.connect(reset_all)

# 滑块值改变时更新标签
def update_volume_label(value):
    volume_label.setText(f"{value}%")

def update_brightness_label(value):
    brightness_label.setText(f"{value}%")

def update_contrast_label(value):
    contrast_label.setText(f"{value}%")

volume_slider.valueChanged.connect(update_volume_label)
brightness_slider.valueChanged.connect(update_brightness_label)
contrast_slider.valueChanged.connect(update_contrast_label)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
