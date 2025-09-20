from rx.subject import Subject
from ultralytics import YOLO
from data_center.index import get_data_center
from utils.yolo.utils import get_device


subject = Subject()

def get_yolo_model_state_subject():
    return subject

def use_yolo_model_path_subject(model_path: str):
    subject.on_next(model_path)

def set_class_info(model: YOLO):
    class_names = list(model.names.values())
    class_ids = list(model.names.keys())
    print(f"模型类别名称: {class_names}")
    print(f"模型类别ID: {class_ids}")
    get_data_center().state.yolo_model_state.update_state(model_class_names=class_names, model_class_ids=class_ids)
    print(f"✅ 模型类别信息设置成功")

def set_yolo_model_state_results(model_path: str = None):
    model = YOLO(model_path)
    model.to(get_device())
    print(f"使用设备: {get_device()}")
    
    get_data_center().state.yolo_model_state.update_state(model=model)
    print(f"✅ 模型加载成功: {model_path}")
    # 设置模型类别信息
    set_class_info(model)


def init_yolo_model_state_subject():
    """初始化YOLO模型状态订阅"""
    subject.subscribe(set_yolo_model_state_results)

init_yolo_model_state_subject()


if __name__ == "__main__":
    use_yolo_model_path_subject("runs/aimlab_fast/weights/best.pt")
