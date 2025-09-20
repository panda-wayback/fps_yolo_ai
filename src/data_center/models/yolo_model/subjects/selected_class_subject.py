from rx.subject import Subject
from typing import List, Optional
from data_center.index import get_data_center


subject = Subject()

def get_yolo_selected_class_subject():
    """获取YOLO选中类别话题"""
    return subject

def use_yolo_selected_class_subject(selected_class_ids: List[int]):
    """发送选中的类别ID"""
    subject.on_next(selected_class_ids)

def update_selected_class_ids(selected_class_ids: List[int]):
    """更新选中的类别ID到状态中"""
    try:
        # 验证类别ID是否有效
        yolo_state = get_data_center().state.yolo_model_state
        if yolo_state.model_class_ids is not None:
            # 检查选中的类别ID是否在模型支持的类别中
            valid_ids = [class_id for class_id in selected_class_ids if class_id in yolo_state.model_class_ids]
            if len(valid_ids) != len(selected_class_ids):
                invalid_ids = [class_id for class_id in selected_class_ids if class_id not in yolo_state.model_class_ids]
                print(f"⚠️ 警告: 以下类别ID无效: {invalid_ids}")
            
            # 更新状态
            get_data_center().state.yolo_model_state.update_state(selected_class_ids=valid_ids)
            print(f"✅ 选中类别已更新: {valid_ids}")
        else:
            print("❌ 模型未加载，无法设置选中类别")
    except Exception as e:
        print(f"❌ 更新选中类别失败: {str(e)}")

def init_yolo_selected_class_subject():
    """初始化YOLO选中类别话题订阅"""
    subject.subscribe(update_selected_class_ids)

# 自动初始化
init_yolo_selected_class_subject()

if __name__ == "__main__":
    # 测试用例
    use_yolo_selected_class_subject([0, 1, 2])
