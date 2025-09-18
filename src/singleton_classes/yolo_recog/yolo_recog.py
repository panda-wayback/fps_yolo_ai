"""
YOLO识别单例类 - 简单易用的目标检测
提供统一的YOLO模型加载和推理接口
"""

import time
import threading
import torch
import numpy as np
from threading import Lock
from typing import List
from ultralytics import YOLO
from data_center.index import get_data_center
from data_center.models.yolo_model.subjects.subject import get_yolo_model_state_subject
from singleton_classes.data_center import DataCenter



class YoloRecog:
    """YOLO识别单例类 - 线程安全的模型管理"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化YOLO模型"""
        if self._initialized:
            return
        
        self._initialized = True
    
    def get_state(self):
        """获取当前YOLO模型状态（实时更新）"""
        return get_data_center().state.yolo_model_state
        
    def load_model(self, model_path: str) -> bool:
        """
        加载YOLO模型
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            get_yolo_model_state_subject().on_next(model_path)

            return True
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False
    
    def detect(self, image: np.ndarray, conf_threshold: float = 0.5) -> List[dict]:
        """
        对图像进行目标检测
        
        Args:
            image: 输入图像 (numpy数组)
            conf_threshold: 置信度阈值
            
        Returns:
            List[dict]: 检测结果列表，每个元素包含:
                - bbox: 边界框 [x1, y1, x2, y2]
                - conf: 置信度
                - cls: 类别ID
                - name: 类别名称
        """
        if self.get_state().model is None:
            print("❌ 模型未加载，请先调用 load_model()")
            return []
        
        try:
            # 执行推理
            results = self.model(image, conf=conf_threshold, verbose=False)
            return results
            
        except Exception as e:
            print(f"❌ 检测失败: {e}")
            return []

    



if __name__ == "__main__":
    # 测试代码
    print("=== YOLO识别单例测试 ===")
    
    # 获取单例实例
    yolo = YoloRecog() 
    # 加载模型
    if  YoloRecog().load_model("runs/aimlab_fast/weights/best.pt"):
        print("✅ 模型加载成功")
        # print(f"模型信息: {yolo.get_model_info()}")
        print(f"类别名称: {yolo.get_state().model_class_names}")
        print(f"类别ID: {yolo.get_state().model_class_ids}")
        # print(f"标签信息: {yolo.print_model_labels()}")

    else:
        print("❌ 模型加载失败")
 