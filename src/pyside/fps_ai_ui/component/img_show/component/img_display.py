#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片展示组件
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage
from pyside.UI.basic.basic_layout import create_vertical_card
import cv2
import numpy as np

from singleton_classes.data_center import DataCenter


def create_img_display():
    """
    创建图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    # 创建主容器
    group = create_vertical_card("图片展示")
    layout = group._layout
    
    # 图片标签
    img_label = QLabel()
    img_label.setAlignment(Qt.AlignCenter)
    img_label.setMinimumSize(400, 300)
    img_label.setText("暂无图片")
    img_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")
    
    layout.addWidget(img_label)
    
    last_image_id = None
    
    def set_image(img_array):
        """设置图片"""
        if img_array is not None:
            # 如果是BGR格式，转换为RGB
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = img_array
            
            # 转换为QImage
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # 转换为QPixmap并显示
            pixmap = QPixmap.fromImage(qt_image)
            img_label.setPixmap(pixmap)
        else:
            img_label.clear()
            img_label.setText("暂无图片")
    
    def bind_to_data_center(get_image_func):
        """绑定到图像获取函数"""
        nonlocal last_image_id
        
        # 创建定时器，定期检查图像变化
        update_timer = QTimer()
        
        def check_image_update():
            """检查图像是否更新"""
            nonlocal last_image_id
            
            try:
                # 调用函数获取最新图像
                current_image = get_image_func()
                
                if current_image is not None:
                    # 使用图像的内存地址作为唯一标识
                    current_id = id(current_image)
                    
                    # 如果图像发生变化，更新显示
                    if current_id != last_image_id:
                        last_image_id = current_id
                        set_image(current_image)
                else:
                    if last_image_id is not None:
                        last_image_id = None
                        img_label.clear()
                        img_label.setText("暂无图片")
            except Exception as e:
                print(f"图像更新错误: {e}")
        
        # 连接定时器
        update_timer.timeout.connect(check_image_update)
        update_timer.start(33)  # 30fps更新
        
        # 存储定时器引用
        group.update_timer = update_timer
    
    # 存储引用到组件
    group.set_image = set_image
    group.bind_to_data_center = bind_to_data_center
    group.img_label = img_label
    
    return group


def get_img_display():
    """
    获取图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    return create_img_display()