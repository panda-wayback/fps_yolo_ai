#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片展示组件
提供图片显示、缩放、保存等功能
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, 
                               QFileDialog, QScrollArea, QVBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from pyside.UI.basic.basic_layout import create_vertical_card
import os
import cv2
import numpy as np


def create_img_display():
    """
    创建图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    # 创建主容器
    group = create_vertical_card("图片展示")
    layout = group._layout
    
    # 图片显示区域
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumSize(400, 300)
    
    # 图片标签
    img_label = QLabel()
    img_label.setAlignment(Qt.AlignCenter)
    img_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")
    img_label.setText("暂无图片")
    img_label.setMinimumSize(400, 300)
    
    scroll_area.setWidget(img_label)
    layout.addWidget(scroll_area)
    
    # 按钮布局
    button_layout = QHBoxLayout()
    
    # 加载图片按钮
    load_btn = QPushButton("加载图片")
    
    # 保存图片按钮
    save_btn = QPushButton("保存图片")
    save_btn.setEnabled(False)
    
    # 清除图片按钮
    clear_btn = QPushButton("清除")
    clear_btn.setEnabled(False)
    
    # 缩放按钮
    zoom_in_btn = QPushButton("放大")
    zoom_in_btn.setEnabled(False)
    
    zoom_out_btn = QPushButton("缩小")
    zoom_out_btn.setEnabled(False)
    
    button_layout.addWidget(load_btn)
    button_layout.addWidget(save_btn)
    button_layout.addWidget(clear_btn)
    button_layout.addWidget(zoom_in_btn)
    button_layout.addWidget(zoom_out_btn)
    
    layout.addLayout(button_layout)
    
    # 存储当前图片和缩放比例
    current_image = None
    current_scale = 1.0
    
    def load_image():
        """加载图片"""
        nonlocal current_image, current_scale
        
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择图片文件",
            "",
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                # 使用OpenCV读取图片
                img = cv2.imread(file_path)
                if img is not None:
                    # 转换颜色格式 BGR -> RGB
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    current_image = img_rgb
                    current_scale = 1.0
                    
                    # 显示图片
                    display_image(img_rgb, 1.0)
                    
                    # 启用按钮
                    save_btn.setEnabled(True)
                    clear_btn.setEnabled(True)
                    zoom_in_btn.setEnabled(True)
                    zoom_out_btn.setEnabled(True)
                    
                    print(f"✅ 加载图片: {os.path.basename(file_path)}")
                else:
                    print("❌ 无法读取图片文件")
            except Exception as e:
                print(f"❌ 加载图片失败: {e}")
    
    def save_image():
        """保存图片"""
        if current_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "保存图片",
                "",
                "图片文件 (*.jpg *.jpeg *.png *.bmp);;所有文件 (*.*)"
            )
            
            if file_path:
                try:
                    # 转换颜色格式 RGB -> BGR
                    img_bgr = cv2.cvtColor(current_image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(file_path, img_bgr)
                    print(f"✅ 保存图片: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"❌ 保存图片失败: {e}")
    
    def clear_image():
        """清除图片"""
        nonlocal current_image, current_scale
        
        current_image = None
        current_scale = 1.0
        
        img_label.clear()
        img_label.setText("暂无图片")
        
        # 禁用按钮
        save_btn.setEnabled(False)
        clear_btn.setEnabled(False)
        zoom_in_btn.setEnabled(False)
        zoom_out_btn.setEnabled(False)
        
        print("🔄 清除图片")
    
    def zoom_in():
        """放大图片"""
        nonlocal current_scale
        
        if current_image is not None:
            current_scale *= 1.2
            display_image(current_image, current_scale)
            print(f"🔍 放大图片: {current_scale:.1f}x")
    
    def zoom_out():
        """缩小图片"""
        nonlocal current_scale
        
        if current_image is not None:
            current_scale /= 1.2
            if current_scale < 0.1:
                current_scale = 0.1
            display_image(current_image, current_scale)
            print(f"🔍 缩小图片: {current_scale:.1f}x")
    
    def display_image(img, scale):
        """显示图片"""
        if img is None:
            return
        
        # 计算缩放后的尺寸
        height, width = img.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 缩放图片
        resized_img = cv2.resize(img, (new_width, new_height))
        
        # 转换为QImage
        h, w, ch = resized_img.shape
        bytes_per_line = ch * w
        qt_image = QImage(resized_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # 转换为QPixmap并显示
        pixmap = QPixmap.fromImage(qt_image)
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(False)
    
    def set_image_from_array(img_array):
        """从numpy数组设置图片"""
        nonlocal current_image, current_scale
        
        if img_array is not None:
            current_image = img_array
            current_scale = 1.0
            display_image(img_array, 1.0)
            
            # 启用按钮
            save_btn.setEnabled(True)
            clear_btn.setEnabled(True)
            zoom_in_btn.setEnabled(True)
            zoom_out_btn.setEnabled(True)
    
    # 连接按钮事件
    load_btn.clicked.connect(load_image)
    save_btn.clicked.connect(save_image)
    clear_btn.clicked.connect(clear_image)
    zoom_in_btn.clicked.connect(zoom_in)
    zoom_out_btn.clicked.connect(zoom_out)
    
    # 存储引用到组件
    group.img_label = img_label
    group.scroll_area = scroll_area
    group.set_image_from_array = set_image_from_array
    group.current_image = current_image
    
    return group


def get_img_display():
    """
    获取图片展示组件
    
    Returns:
        QGroupBox: 图片展示组件
    """
    return create_img_display()
