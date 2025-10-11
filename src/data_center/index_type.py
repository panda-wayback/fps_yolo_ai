
from typing import Optional
from pydantic import BaseModel
from data_center.models.base_state import BaseState

from data_center.models.screenshot.model import ScreenshotModel
from data_center.models.controller_model.model import ControllerModel
from data_center.models.yolo_model.model import YoloModel
from data_center.models.mouse_driver_model.model import MouseDriverModel
from data_center.models.target_selector.model import TargetSelectorModel
from data_center.models.input_monitor.model import InputMonitorModel



class User(BaseState):
    name: Optional[str] = None
    age: Optional[int] = None

class Order(BaseState):
    name: Optional[str] = None
    price: Optional[int] = None


class State(BaseModel):
    user: Optional[User] = User()
    order: Optional[Order] = Order()
    yolo_model_state: Optional[YoloModel] = YoloModel()
    screenshot_state: Optional[ScreenshotModel] = ScreenshotModel()
    controller_model_state: Optional[ControllerModel] = ControllerModel()
    mouse_driver_state: Optional[MouseDriverModel] = MouseDriverModel()
    target_selector_state: Optional[TargetSelectorModel] = TargetSelectorModel()
    input_monitor_state: Optional[InputMonitorModel] = InputMonitorModel()