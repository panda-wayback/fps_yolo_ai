from dataclasses import dataclass, asdict
from typing import Optional, Tuple, Any, Dict, List
import numpy as np
import json
import base64

@dataclass
class State:
    test_text: str = "test"
    screenshot_img: Optional[np.ndarray] = None
    mouse_pos: Optional[Tuple[int, int]] = None
    region: Optional[Tuple[int, int]] = None
    yolo_results: Optional[List[Any]] = None
    
    # 标记过目标的图片
    marked_img: Optional[np.ndarray] = None
    
    # YOLO模型类别相关数据
    model_class_names: Optional[List[str]] = None  # 模型的所有类别名称
    model_class_ids: Optional[List[int]] = None    # 模型的所有类别ID
    selected_class_ids: Optional[List[int]] = None # 当前选择的要识别的类别ID
    model_path: Optional[str] = None               # 当前加载的模型路径

    def to_dict(self) -> Dict[str, Any]:
        """
        将State转换为字典，处理numpy数组的序列化
        """
        data = asdict(self)
        
        # 处理numpy数组
        if data['screenshot_img'] is not None:
            # 将numpy数组转换为base64字符串
            img_bytes = data['screenshot_img'].tobytes()
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')
            data['screenshot_img'] = {
                'data': img_b64,
                'shape': data['screenshot_img'].shape,
                'dtype': str(data['screenshot_img'].dtype)
            }
        
        return data
    
    def to_json(self) -> str:
        """
        将State转换为JSON字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'State':
        """
        从字典创建State实例，处理numpy数组的反序列化
        """
        # 处理numpy数组
        if data.get('screenshot_img') is not None and isinstance(data['screenshot_img'], dict):
            img_info = data['screenshot_img']
            img_bytes = base64.b64decode(img_info['data'])
            data['screenshot_img'] = np.frombuffer(img_bytes, dtype=img_info['dtype']).reshape(img_info['shape'])
        
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'State':
        """
        从JSON字符串创建State实例
        """
        data = json.loads(json_str)
        return cls.from_dict(data)