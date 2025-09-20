#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO模型状态展示组件
显示模型加载状态和基本信息
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from pyside.UI.basic.basic_layout import create_vertical_card

from data_center.models.yolo_model.subject import YoloSubject


def create_yolo_model_state():
    """
    创建YOLO模型状态展示组件
    
    Returns:
        QGroupBox: YOLO模型状态组件
    """
    # 创建主容器
    group = create_vertical_card("YOLO模型状态")
    layout = group._layout
    
    # 设置最小宽度，防止被挤压
    group.setMinimumWidth(200)
    
    # 状态标签
    status_label = QLabel("状态: 未加载")
    status_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
    
    # 模型信息标签
    info_label = QLabel("")
    info_label.setStyleSheet("color: blue; font-size: 12px;")
    info_label.setWordWrap(True)
    
    # 结果信息标签
    result_label = QLabel("")
    result_label.setStyleSheet("color: green; font-size: 11px;")
    result_label.setWordWrap(True)
    
    layout.addWidget(status_label)
    layout.addWidget(info_label)
    layout.addWidget(result_label)
    
    # 更新状态显示
    def update_status():
        """更新状态显示"""
        try:
            yolo_state = YoloSubject.get_yolo_model_state()
            
            if yolo_state.model is not None:
                # 模型已加载
                status_label.setText("状态: 已加载")
                status_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
                
                # 显示模型信息
                model_path = yolo_state.model_path or "未知路径"
                class_count = len(yolo_state.model_class_names) if yolo_state.model_class_names else 0
                info_text = f"模型: {model_path.split('/')[-1]}\n类别数量: {class_count}"
                
                if yolo_state.model_class_names:
                    info_text += f"\n类别: {', '.join(yolo_state.model_class_names[:3])}"
                    if len(yolo_state.model_class_names) > 3:
                        info_text += "..."
                
                info_label.setText(info_text)
                
                # 显示检测结果信息
                if yolo_state.yolo_results:
                    result_count = len(yolo_state.yolo_results)
                    result_text = f"检测结果: {result_count} 个目标"
                    if yolo_state.selected_class_ids:
                        result_text += f"\n选中类别: {yolo_state.selected_class_ids}"
                    result_label.setText(result_text)
                else:
                    result_label.setText("检测结果: 无")
                    
            else:
                # 模型未加载
                status_label.setText("状态: 未加载")
                status_label.setStyleSheet("color: gray; font-size: 14px; font-weight: bold;")
                info_label.setText("")
                result_label.setText("")
                
        except Exception as e:
            status_label.setText("状态: 错误")
            status_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
            info_label.setText(f"错误: {str(e)}")
            result_label.setText("")
    
    # 定时更新状态
    timer = QTimer()
    timer.timeout.connect(update_status)
    timer.start(1000)  # 每秒更新一次
    
    # 立即更新一次
    update_status()
    
    # 存储引用
    group.update_status = update_status
    group.timer = timer
    
    return group


def get_yolo_model_state():
    """
    获取YOLO模型状态组件
    
    Returns:
        QGroupBox: YOLO模型状态组件
    """
    return create_yolo_model_state()
