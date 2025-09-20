"""
YOLO选中类别话题处理
基于PID模型的最佳实践
"""

from typing import List, Optional
from data_center.index import get_data_center
from data_center.models.yolo_model.subject_model import YoloSubjectModel


def update_selected_class_ids(selected_class_ids: List[int]):
    """更新选中的类别ID"""
    try:
        # 更新数据中心状态
        state = get_data_center().state.yolo_model_state
        state.selected_class_ids = selected_class_ids
        
        print(f"✅ 已设置选中类别: {selected_class_ids}")
        
        # 如果模型已加载，可以在这里添加额外的处理逻辑
        if state.model is not None:
            print(f"模型已加载，类别设置生效")
        else:
            print("❌ 模型未加载，无法设置选中类别")
            
    except Exception as e:
        print(f"❌ 更新选中类别失败: {str(e)}")


def init_selected_class_subject():
    """初始化YOLO选中类别订阅"""
    YoloSubjectModel.selected_class_subject.subscribe(update_selected_class_ids)


init_selected_class_subject()


if __name__ == "__main__":
    # 测试用例
    YoloSubjectModel.selected_class_subject.on_next([0, 1, 2])