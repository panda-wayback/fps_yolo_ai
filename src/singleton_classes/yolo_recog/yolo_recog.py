"""
YOLO识别单例类 - 简单易用的目标检测
提供统一的YOLO模型加载和推理接口
"""
import numpy as np
from threading import Lock
from typing import List

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
        from data_center.models.yolo_model.subject import YoloSubject
        return YoloSubject.get_yolo_model_state()
    
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
            results = self.get_state().model(image, conf=conf_threshold, verbose=False)
            return results
            
        except Exception as e:
            print(f"❌ 检测失败: {e}")
            return []

_yolo_recog = YoloRecog()
def get_yolo_recog():
    return _yolo_recog

if __name__ == "__main__":
    # 测试代码
    print("=== YOLO识别单例测试 ===")
    