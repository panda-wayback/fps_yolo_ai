"""
YOLO模型加载话题处理
基于PID模型的最佳实践
"""

from ultralytics import YOLO
from data_center.index import get_data_center


def set_class_info(model: YOLO):
    """设置模型类别信息"""
    try:
        class_names = list(model.names.values())
        class_ids = list(model.names.keys())
        print(f"模型类别名称: {class_names}")
        
        # 更新数据中心状态
        state = get_data_center().state.yolo_model_state
        state.model_class_names = class_names
        state.model_class_ids = class_ids
    except Exception as e:
        print(f"设置模型类别信息失败: {e}")


def set_yolo_model_state_results(model_path: str):
    """设置YOLO模型状态"""
    try:
        print(f"🔄 正在加载YOLO模型: {model_path}")
        
        # 加载模型
        model = YOLO(model_path)
        
        # 更新数据中心状态
        state = get_data_center().state.yolo_model_state
        state.model = model
        state.model_path = model_path
        
        print(f"✅ 模型加载成功: {model_path}")
        
        # 设置模型类别信息
        set_class_info(model)
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")




if __name__ == "__main__":
    # 测试用例
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_model_path("runs/aimlab_fast/weights/best.pt")