from rx.subject import Subject
from ultralytics import YOLO
from data_center.index import get_data_center
from data_center.models.yolo_model.state import YoloModelState

subject = Subject()

def get_yolo_model_state_subject():
    return subject


def set_yolo_model_state_results(model_path: str = None):

    try:
        model = YOLO(model_path)
        if model is None:
            print(f"❌ 模型加载失败: {model_path}")
            return
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return
    
    get_data_center().state.yolo_model_state.update_state(model=model)

    print(f"✅ 模型加载成功: {model_path}")
    print(f"模型类别名称: {model.names.values()}")
    print(f"模型类别ID: {model.names.keys()}")
    
    class_names = model.names.values()
    class_ids = model.names.keys()
    get_data_center().state.yolo_model_state.update_state(model_class_names=class_names, model_class_ids=class_ids)



if __name__ == "__main__":
    subject.subscribe(set_yolo_model_state_results)

    subject.on_next("runs/aimlab_fast/weights/best.pt")
