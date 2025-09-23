#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO标记图片显示组件
持续显示标记过目标的图片
"""

from PySide6.QtWidgets import QLabel, QScrollArea
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QImage
import numpy as np
from pyside.UI.basic.basic_layout import create_vertical_card

from data_center.models.yolo_model.state import YoloModelState


def create_yolo_marked_image():
    """
    创建YOLO标记图片显示组件
    
    Returns:
        QGroupBox: YOLO标记图片显示组件
    """
    # 创建主容器
    group = create_vertical_card("标记图片")
    layout = group._layout
    
    # 状态标签
    status_label = QLabel("等待图片...")
    status_label.setStyleSheet("color: gray; font-size: 12px;")
    
    # 图片显示标签
    image_label = QLabel()
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setMinimumSize(320, 240)
    image_label.setStyleSheet("""
        QLabel {
            border: 2px solid #ccc;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
    """)
    image_label.setText("暂无图片")
    
    # 图片信息标签
    info_label = QLabel("")
    info_label.setStyleSheet("color: blue; font-size: 11px;")
    info_label.setWordWrap(True)
    
    # 滚动区域（用于大图片）
    scroll_area = QScrollArea()
    scroll_area.setWidget(image_label)
    scroll_area.setWidgetResizable(True)
    scroll_area.setMaximumHeight(400)
    scroll_area.setMinimumHeight(200)
    
    # 存储上次的图片数据，用于检测变化
    last_image_hash = None
    last_update_time = 0
    
    # 更新图片显示
    def update_image():
        """更新图片显示"""
        nonlocal last_image_hash, last_update_time
        
        try:
            from utils.image_converter import ImageConverter
            
            yolo_state = YoloModelState.get_state()
            marked_img = yolo_state.marked_img.get()
            
            if marked_img is not None:
                # 有标记图片
                # 使用新的转换工具计算图片哈希值
                current_hash = ImageConverter.get_image_hash(marked_img)
                
                # 获取图片信息
                img_info = ImageConverter.get_image_info(marked_img)
                
                # 检查图片是否发生变化
                image_changed = current_hash != last_image_hash
                
                if image_changed:
                    last_image_hash = current_hash
                    last_update_time = 0  # 重置时间
                    # print(f"🔄 检测到新图片: {img_info['width']}x{img_info['height']}, 通道: {img_info['channels']}")
                else:
                    # 图片未变化，增加时间计数
                    last_update_time += 1
                
                # 更新状态
                status_text = "✅ 显示标记图片"
                if image_changed:
                    status_text += " (新图片)"
                else:
                    status_text += f" (刷新: {last_update_time})"
                status_label.setText(status_text)
                status_label.setStyleSheet("color: green; font-size: 12px;")
                
                # 更新图片信息
                info_text = f"尺寸: {img_info['width']}x{img_info['height']}\n通道: {img_info['channels']}"
                yolo_results = yolo_state.yolo_results.get()
                if yolo_results:
                    info_text += f"\n检测目标: {len(yolo_results)} 个"
                info_text += f"\n刷新次数: {last_update_time}"
                info_label.setText(info_text)
                
                # 只有在图片发生变化时才重新绘制
                if image_changed:
                    # 使用新的转换工具转换为Qt格式
                    target_size = (image_label.size().width(), image_label.size().height())
                    pixmap = ImageConverter.convert_for_display(
                        marked_img, 
                        target_format="qt", 
                        target_size=target_size, 
                        keep_aspect_ratio=True
                    )
                    
                    if pixmap is not None:
                        image_label.setPixmap(pixmap)
                        image_label.setText("")  # 清除文本
                    else:
                        print("❌ 图片转换失败")
                
            else:
                # 没有标记图片
                status_label.setText("等待图片...")
                status_label.setStyleSheet("color: gray; font-size: 12px;")
                
                image_label.clear()
                image_label.setText("暂无图片")
                info_label.setText("")
                
                # 重置状态
                last_image_hash = None
                last_update_time = 0
                
        except Exception as e:
            status_label.setText(f"❌ 显示错误: {str(e)}")
            status_label.setStyleSheet("color: red; font-size: 12px;")
            print(f"❌ 更新标记图片失败: {str(e)}")
    
    # 定时更新图片 - 提高刷新频率以更好地响应后台变化
    timer = QTimer()
    timer.timeout.connect(update_image)
    timer.start(50)  # 每50ms更新一次，20FPS
    
    # 立即更新一次
    update_image()
    
    # 添加到布局
    layout.addWidget(status_label)
    layout.addWidget(scroll_area)
    layout.addWidget(info_label)
    
    # 存储引用
    group.update_image = update_image
    group.timer = timer
    group.image_label = image_label
    
    return group


def get_yolo_marked_image():
    """
    获取YOLO标记图片显示组件
    
    Returns:
        QGroupBox: YOLO标记图片显示组件
    """
    return create_yolo_marked_image()

