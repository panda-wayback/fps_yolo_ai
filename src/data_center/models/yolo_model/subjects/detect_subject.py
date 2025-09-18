
from rx.subject import BehaviorSubject
from data_center.index import get_data_center

import numpy as np

from data_center.models.yolo_model.index import YoloModelState
from singleton_classes.yolo_recog.yolo_recog import YoloRecog

detect_subject = BehaviorSubject( None)

state = get_data_center().state.yolo_model_state

def get_detect_subject():
    return detect_subject


def set_detect_subject(value:np.ndarray = None):
    result = YoloRecog().detect(value)
    state.yolo_results = result

if __name__ == "__main__":
    detect_subject.subscribe(set_detect_subject)
    detect_subject.on_next(YoloModelState(yolo_results=[1, 2, 3]))
