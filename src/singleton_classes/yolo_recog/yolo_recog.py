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

from functions.ims_show import get_yolo_image
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
            
        self.model = None
        self.device = self._get_device()
        self.model_path = None
        self._initialized = True
        self._is_running = False
        self._yolo_thread = None
        print(f"YoloRecog 单例初始化完成，使用设备: {self.device}")
    
    def _get_device(self) -> str:
        """获取最佳计算设备"""
        if torch.backends.mps.is_available():
            return 'mps'
        elif torch.cuda.is_available():
            return 'cuda'
        else:
            return 'cpu'
    
    def start(self, yolo_model_path: str):
        """
        开始YOLO循环
        """
        print(f"开始YOLO循环, 模型路径: {yolo_model_path}")
        
        if self._is_running:
            self.stop()
            time.sleep(0.1)
        
        self._is_running = True
        self.model_path = yolo_model_path
        
        # 先加载模型
        if self.load_model(yolo_model_path):
            # 模型加载成功后更新DataCenter
            self._update_model_info_to_datacenter()
            
            self._yolo_thread = threading.Thread(target=self._yolo_loop)
            self._yolo_thread.start()
        else:
            print("❌ 模型加载失败，无法启动YOLO循环")
            self._is_running = False
    
    def stop(self):
        """
        停止YOLO循环
        """
        self._is_running = False
        if self._yolo_thread:
            self._yolo_thread.join(timeout=1.0)

    def _yolo_loop(self):
        """
        YOLO循环
        """
        last_img = None
        while self._is_running:
            try:
            # 如果截图为空，或者截图重复，则不进行检测
                current_img = DataCenter().get_state().screenshot_img
                if current_img is None:
                    time.sleep(0.001)
                    continue
                
                # 使用numpy的array_equal来比较数组
                if last_img is not None and np.array_equal(current_img, last_img):
                    time.sleep(0.001)
                    continue
                
                last_img = current_img
                # 检测
                results = self.detect(current_img, 0.5)
                # 图像处理
                result_img = get_yolo_image(current_img, results)
                # 更新状态
                DataCenter().update_state(marked_img=result_img)

            except Exception as e:
                print(f"❌ YOLO循环错误: {e}")

            time.sleep(0.001)
    
    def load_model(self, model_path: str) -> bool:
        """
        加载YOLO模型
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            print(f"正在加载YOLO模型: {model_path}")
            self.model = YOLO(model_path)
            self.model.to(self.device)
            self.model_path = model_path
            print(f"✅ 模型加载成功，使用设备: {self.device}")
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
        if self.model is None:
            print("❌ 模型未加载，请先调用 load_model()")
            return []
        
        try:
            # 执行推理
            results = self.model(image, conf=conf_threshold, verbose=False)
            return results
            
        except Exception as e:
            print(f"❌ 检测失败: {e}")
            return []

    
    def detect_center(self, image: np.ndarray, conf_threshold: float = 0.5) -> List[dict]:
        """
        检测目标并返回中心点坐标
        
        Args:
            image: 输入图像
            conf_threshold: 置信度阈值
            
        Returns:
            List[dict]: 包含中心点坐标的检测结果
        """
        detections = self.detect(image, conf_threshold)
        
        # 为每个检测结果添加中心点坐标
        for detection in detections:
            bbox = detection['bbox']
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            detection['center'] = [center_x, center_y]
        
        return detections
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        if self.model is None:
            return {"status": "未加载"}
        
        return {
            "status": "已加载",
            "model_path": self.model_path,
            "device": self.device,
            "class_names": list(self.model.names.values()) if hasattr(self.model, 'names') else []
        }
    
    def get_class_names(self) -> List[str]:
        """获取模型的所有类别名称"""
        if self.model is None:
            return []
        
        if hasattr(self.model, 'names'):
            return list(self.model.names.values())
        return []
    
    def get_class_ids(self) -> List[int]:
        """获取模型的所有类别ID"""
        if self.model is None:
            return []
        
        if hasattr(self.model, 'names'):
            return list(self.model.names.keys())
        return []
    
    def print_model_labels(self):
        """打印模型的所有标签信息"""
        if self.model is None:
            print("❌ 模型未加载，无法获取标签信息")
            return
        
        print("=" * 50)
        print("📋 YOLO模型标签信息")
        print("=" * 50)
        print(f"模型路径: {self.model_path}")
        print(f"设备: {self.device}")
        print(f"总类别数: {len(self.model.names) if hasattr(self.model, 'names') else 0}")
        print()
        
        if hasattr(self.model, 'names'):
            print("🏷️  类别标签列表:")
            for class_id, class_name in self.model.names.items():
                print(f"  {class_id:2d}: {class_name}")
        else:
            print("❌ 无法获取类别信息")
        print("=" * 50)
    
    def is_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self.model is not None
    
    def _update_model_info_to_datacenter(self):
        """更新DataCenter中的模型信息"""
        if self.model is None:
            return
        
        try:
            class_names = self.get_class_names()
            class_ids = self.get_class_ids()
            
            DataCenter().update_state(
                model_class_names=class_names,
                model_class_ids=class_ids,
                model_path=self.model_path,
                selected_class_ids=class_ids  # 默认选择所有类别
            )
            
            print(f"✅ 已更新DataCenter模型信息: {len(class_names)}个类别")
            print(f"类别名称: {class_names}")
            print(f"类别ID: {class_ids}")
            
        except Exception as e:
            print(f"❌ 更新DataCenter模型信息失败: {e}")



if __name__ == "__main__":
    # 测试代码
    print("=== YOLO识别单例测试 ===")
    
    # 获取单例实例
    yolo = YoloRecog()
    print(f"模型信息: {yolo.get_model_info()}")
   
    # 加载模型
    if  YoloRecog().load_model("runs/aimlab_fast/weights/best.pt"):
        print("✅ 模型加载成功")
        # print(f"模型信息: {yolo.get_model_info()}")
        print(f"类别名称: {yolo.get_class_names()}")
        print(f"类别ID: {yolo.get_class_ids()}")
        # print(f"标签信息: {yolo.print_model_labels()}")

    else:
        print("❌ 模型加载失败")
 