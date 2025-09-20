#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO类别选择组件
允许用户选择需要识别的类别编号
"""

from PySide6.QtWidgets import (QCheckBox, QScrollArea, QWidget, 
                               QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PySide6.QtCore import QTimer
from pyside.UI.basic.basic_layout import create_vertical_card

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
    
    # 全选按钮
    select_all_btn = QPushButton("全选")
    select_all_btn.setEnabled(False)
    
    # 全不选按钮
    select_none_btn = QPushButton("全不选")
    select_none_btn.setEnabled(False)
    
    # 应用按钮
    apply_btn = QPushButton("应用选择")
    apply_btn.setEnabled(False)
    
    button_layout.addWidget(select_all_btn)
    button_layout.addWidget(select_none_btn)
    button_layout.addWidget(apply_btn)
    
    # 存储复选框引用
    checkboxes = {}
    
    # 更新类别列表
    def update_classes():
        """更新类别列表"""
        try:
            yolo_state = YoloSubject.get_yolo_model_state()
            
            if yolo_state.model is not None and yolo_state.model_class_names is not None:
                # 模型已加载，显示类别
                status_label.setText(f"已加载 {len(yolo_state.model_class_names)} 个类别")
                status_label.setStyleSheet("color: green; font-size: 12px;")
                
                # 清除旧的复选框
                for checkbox in checkboxes.values():
                    checkbox.deleteLater()
                checkboxes.clear()
                
                # 创建新的复选框
                for i, class_name in enumerate(yolo_state.model_class_names):
                    checkbox = QCheckBox(f"{i}: {class_name}")
                    checkbox.setChecked(True)  # 默认全选
                    checkboxes[i] = checkbox
                    scroll_layout.addWidget(checkbox)
                
                # 启用按钮
                select_all_btn.setEnabled(True)
                select_none_btn.setEnabled(True)
                apply_btn.setEnabled(True)
                
            else:
                # 模型未加载
                status_label.setText("等待模型加载...")
                status_label.setStyleSheet("color: gray; font-size: 12px;")
                
                # 清除复选框
                for checkbox in checkboxes.values():
                    checkbox.deleteLater()
                checkboxes.clear()
                
                # 禁用按钮
                select_all_btn.setEnabled(False)
                select_none_btn.setEnabled(False)
                apply_btn.setEnabled(False)
                
        except Exception as e:
            status_label.setText(f"错误: {str(e)}")
            status_label.setStyleSheet("color: red; font-size: 12px;")
    
    # 全选功能
    def select_all():
        """全选所有类别"""
        for checkbox in checkboxes.values():
            checkbox.setChecked(True)
        print("✅ 已全选所有类别")
    
    # 全不选功能
    def select_none():
        """全不选所有类别"""
        for checkbox in checkboxes.values():
            checkbox.setChecked(False)
        print("🔄 已取消选择所有类别")
    
    # 应用选择功能
    def apply_selection():
        """应用选择的类别"""
        selected_ids = []
        for class_id, checkbox in checkboxes.items():
            if checkbox.isChecked():
                selected_ids.append(class_id)
        
        if selected_ids:
            YoloSubject.send_selected_class_ids(selected_ids)
            print(f"✅ 已应用选择的类别: {selected_ids}")
        else:
            print("⚠️ 未选择任何类别")
    
    # 连接按钮事件
    select_all_btn.clicked.connect(select_all)
    select_none_btn.clicked.connect(select_none)
    apply_btn.clicked.connect(apply_selection)
    
    # 定时更新类别列表
    timer = QTimer()
    timer.timeout.connect(update_classes)
    timer.start(1000)  # 每秒更新一次
    
    # 立即更新一次
    update_classes()
    
    # 添加到布局
    layout.addWidget(status_label)
    layout.addWidget(scroll_area)
    layout.addLayout(button_layout)
    
    # 存储引用
    group.update_classes = update_classes
    group.timer = timer
    group.checkboxes = checkboxes
    
    return group


def get_yolo_classes_selector():
    """
    获取YOLO类别选择组件
    
    Returns:
        QGroupBox: YOLO类别选择组件
    """
    return create_yolo_classes_selector()
