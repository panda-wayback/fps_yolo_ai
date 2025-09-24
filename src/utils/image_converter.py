"""
图片转换工具类
支持将numpy数组转换为各种显示格式
"""

import numpy as np
from typing import Optional, Union, Tuple
import hashlib

try:
    from PySide6.QtGui import QImage, QPixmap
    from PySide6.QtCore import Qt
    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False

import cv2


class ImageConverter:
    """图片转换工具类"""
    
    @staticmethod
    def convert_for_display(
        img: np.ndarray, 
        target_format: str = "opencv",
        target_size: Optional[Tuple[int, int]] = None,
        keep_aspect_ratio: bool = True
    ) -> Union[np.ndarray, QPixmap, None]:
        """
        将numpy数组转换为可显示的格式
        
        参数:
            img: 输入的numpy数组图片
            target_format: 目标格式 ("opencv", "qt", "auto")
            target_size: 目标尺寸 (width, height)，None表示不缩放
            keep_aspect_ratio: 是否保持宽高比
            
        返回:
            转换后的图片，失败返回None
        """
        try:
            # 验证输入
            if not ImageConverter._validate_image(img):
                return None
            
            # 预处理图片
            processed_img = ImageConverter._preprocess_image(img)
            if processed_img is None:
                return None
            
            # 根据目标格式进行转换
            if target_format == "opencv":
                return ImageConverter._convert_to_opencv(processed_img, target_size, keep_aspect_ratio)
            elif target_format == "qt":
                return ImageConverter._convert_to_qt(processed_img, target_size, keep_aspect_ratio)
            elif target_format == "auto":
                # 自动选择格式
                if QT_AVAILABLE:
                    return ImageConverter._convert_to_qt(processed_img, target_size, keep_aspect_ratio)
                else:
                    return ImageConverter._convert_to_opencv(processed_img, target_size, keep_aspect_ratio)
            else:
                print(f"错误: 不支持的目标格式: {target_format}")
                return None
                
        except Exception as e:
            print(f"图片转换失败: {e}")
            return None
    
    @staticmethod
    def _validate_image(img: np.ndarray) -> bool:
        """验证输入图片的有效性"""
        if img is None:
            print("警告: 输入图片为 None")
            return False
        
        if not isinstance(img, np.ndarray):
            print(f"警告: 输入不是numpy数组，类型为: {type(img)}")
            return False
        
        if img.size == 0:
            print("警告: 输入图片为空数组")
            return False
        
        if len(img.shape) < 2:
            print(f"警告: 图片维度不足，shape: {img.shape}")
            return False
        
        return True
    
    @staticmethod
    def _preprocess_image(img: np.ndarray) -> Optional[np.ndarray]:
        """预处理图片：格式转换、数据类型转换等"""
        try:
            processed_img = img.copy()
            
            # 确保数据类型为uint8
            if processed_img.dtype != np.uint8:
                if processed_img.dtype in [np.float32, np.float64]:
                    # 浮点数，假设范围在0-1之间，转换为0-255
                    if processed_img.max() <= 1.0:
                        processed_img = (processed_img * 255).astype(np.uint8)
                    else:
                        processed_img = processed_img.astype(np.uint8)
                else:
                    processed_img = processed_img.astype(np.uint8)
            
            # 确保是3通道的BGR格式（OpenCV标准）
            if len(processed_img.shape) == 2:
                # 灰度图转BGR
                processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
            elif len(processed_img.shape) == 3:
                if processed_img.shape[2] == 4:
                    # RGBA转BGR
                    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGBA2BGR)
                elif processed_img.shape[2] == 3:
                    # 假设已经是BGR格式
                    pass
                else:
                    print(f"警告: 不支持的通道数: {processed_img.shape[2]}")
                    return None
            
            # 检查转换后的图片尺寸
            if processed_img.shape[0] <= 0 or processed_img.shape[1] <= 0:
                print(f"警告: 转换后图片尺寸无效: {processed_img.shape}")
                return None
            
            return processed_img
            
        except Exception as e:
            print(f"图片预处理失败: {e}")
            return None
    
    @staticmethod
    def _convert_to_opencv(
        img: np.ndarray, 
        target_size: Optional[Tuple[int, int]], 
        keep_aspect_ratio: bool
    ) -> Optional[np.ndarray]:
        """转换为OpenCV显示格式"""
        try:
            if target_size is None:
                return img
            
            # 缩放图片
            if keep_aspect_ratio:
                h, w = img.shape[:2]
                target_w, target_h = target_size
                
                # 计算缩放比例
                scale = min(target_w / w, target_h / h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                
                resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            else:
                resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
            
            return resized_img
            
        except Exception as e:
            print(f"OpenCV格式转换失败: {e}")
            return None
    
    @staticmethod
    def _convert_to_qt(
        img: np.ndarray, 
        target_size: Optional[Tuple[int, int]], 
        keep_aspect_ratio: bool
    ) -> Optional[QPixmap]:
        """转换为Qt显示格式"""
        try:
            if not QT_AVAILABLE:
                print("错误: Qt不可用，无法转换为Qt格式")
                return None
            
            h, w = img.shape[:2]
            
            # 转换为QImage
            # 注意：OpenCV使用BGR，Qt使用RGB
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_img.data, w, h, w * 3, QImage.Format_RGB888)
            
            # 转换为QPixmap
            pixmap = QPixmap.fromImage(q_image)
            
            # 缩放图片
            if target_size is not None:
                if keep_aspect_ratio:
                    scaled_pixmap = pixmap.scaled(
                        target_size[0], target_size[1],
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap = pixmap.scaled(
                        target_size[0], target_size[1],
                        Qt.IgnoreAspectRatio,
                        Qt.SmoothTransformation
                    )
                return scaled_pixmap
            
            return pixmap
            
        except Exception as e:
            print(f"Qt格式转换失败: {e}")
            return None
    
    @staticmethod
    def get_image_hash(img: np.ndarray) -> Optional[str]:
        """获取图片的哈希值，用于检测变化"""
        try:
            if not ImageConverter._validate_image(img):
                return None
            
            return hashlib.md5(img.tobytes()).hexdigest()
        except Exception as e:
            print(f"获取图片哈希失败: {e}")
            return None
    
    @staticmethod
    def get_image_info(img: np.ndarray) -> dict:
        """获取图片信息"""
        try:
            if not ImageConverter._validate_image(img):
                return {}
            
            info = {
                'width': img.shape[1],
                'height': img.shape[0],
                'channels': img.shape[2] if len(img.shape) > 2 else 1,
                'dtype': str(img.dtype),
                'shape': img.shape
            }
            return info
        except Exception as e:
            print(f"获取图片信息失败: {e}")
            return {}


# 便捷函数
def convert_marked_img_for_display(img: np.ndarray, target_format: str = "opencv") -> Union[np.ndarray, QPixmap, None]:
    """
    便捷函数：将YOLO标记的图片转换为可显示格式
    
    参数:
        img: YOLO标记的图片
        target_format: 目标格式 ("opencv", "qt", "auto")
    
    返回:
        转换后的图片，失败返回None
    """
    return ImageConverter.convert_for_display(img, target_format)


def get_displayable_marked_img(target_format: str = "opencv") -> Union[np.ndarray, QPixmap, None]:
    """
    便捷函数：从YoloModelState获取标记图片并转换为可显示格式
    
    参数:
        target_format: 目标格式 ("opencv", "qt", "auto")
    
    返回:
        转换后的图片，失败返回None
    """
    try:
        from data_center.models.yolo_model.state import YoloModelState
        
        # 获取标记图片
        marked_img = YoloModelState.get_state().marked_img.get()
        
        # 转换为可显示格式
        return ImageConverter.convert_for_display(marked_img, target_format)
        
    except Exception as e:
        print(f"获取显示图片失败: {e}")
        return None
