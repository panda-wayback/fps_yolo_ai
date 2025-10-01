#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO类别选择组件
允许用户选择需要识别的类别编号
"""

from PySide6.QtWidgets import (QCheckBox, QScrollArea, QWidget, 
                               QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from pyside.UI.basic.basic_layout import create_vertical_card

from data_center.models.yolo_model.state import YoloModelState
from data_center.models.yolo_model.subject import YoloSubject


def create_yolo_classes_selector():
    """
    创建YOLO类别选择组件
    
    Returns:
        QGroupBox: YOLO类别选择组件
    """
    # 创建主容器
    group = create_vertical_card("类别选择")
    layout = group._layout
    
    # 状态标签
    status_label = QLabel("等待模型加载...")
    status_label.setStyleSheet("color: gray; font-size: 12px;")
    
    # 滚动区域
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setMaximumHeight(200)
    
    # 滚动内容
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_area.setWidget(scroll_content)
    
    # 按钮区域
    button_layout = QHBoxLayout()
    
    # 刷新按钮
    refresh_btn = QPushButton("刷新类别")
    
    # 全选按钮
    select_all_btn = QPushButton("全选")
    
    # 全不选按钮
    select_none_btn = QPushButton("全不选")
    
    # 应用按钮
    apply_btn = QPushButton("应用选择")
    
    button_layout.addWidget(refresh_btn)
    button_layout.addWidget(select_all_btn)
    button_layout.addWidget(select_none_btn)
    button_layout.addWidget(apply_btn)
    
    # 存储复选框引用
    checkboxes = {}
    
    # 加载类别
    def load_classes():
        try:
            yolo_state = YoloModelState.get_state()
            class_names = yolo_state.class_names.get()
            
            if class_names is not None:
                status_label.setText(f"已加载 {len(class_names)} 个类别")
                status_label.setStyleSheet("color: green; font-size: 12px;")
                
                # 清除旧的复选框
                for checkbox in checkboxes.values():
                    checkbox.deleteLater()
                checkboxes.clear()
                
                # 创建复选框
                for i, class_name in enumerate(class_names):
                    checkbox = QCheckBox(f"{i}: {class_name}")
                    checkbox.setChecked(True)  # 默认全选
                    checkboxes[i] = checkbox
                    scroll_layout.addWidget(checkbox)
            else:
                status_label.setText("模型未加载，请先加载模型")
                status_label.setStyleSheet("color: orange; font-size: 12px;")
        except Exception as e:
            status_label.setText(f"错误: {str(e)}")
            status_label.setStyleSheet("color: red; font-size: 12px;")
    
    # 全选功能
    def select_all():
        for checkbox in checkboxes.values():
            checkbox.setChecked(True)
    
    # 全不选功能
    def select_none():
        for checkbox in checkboxes.values():
            checkbox.setChecked(False)
    
    # 应用选择功能
    def apply_selection():
        selected_ids = [class_id for class_id, checkbox in checkboxes.items() if checkbox.isChecked()]
        
        if selected_ids:
            YoloSubject.send_selected_class_ids(selected_ids)
            print(f"✅ 已应用选择的类别: {selected_ids}")
        else:
            print("⚠️ 未选择任何类别")
    
    # 连接按钮事件
    refresh_btn.clicked.connect(load_classes)
    select_all_btn.clicked.connect(select_all)
    select_none_btn.clicked.connect(select_none)
    apply_btn.clicked.connect(apply_selection)
    
    # 添加到布局
    layout.addWidget(status_label)
    layout.addWidget(scroll_area)
    layout.addLayout(button_layout)
    
    return group


def get_yolo_classes_selector():
    """
    获取YOLO类别选择组件
    
    Returns:
        QGroupBox: YOLO类别选择组件
    """
    return create_yolo_classes_selector()
