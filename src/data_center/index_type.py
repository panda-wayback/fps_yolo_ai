
from typing_extensions import Optional
from pydantic import BaseModel
from data_center.models.base_state import BaseState

from data_center.models.screenshot.model import ScreenshotModel
from data_center.models.pid_model.model import PIDModel
from data_center.models.yolo_model.model import YoloModel
from data_center.models.mouse_driver_model.state_model import MouseDriverState
from data_center.models.target_selector.state_model import TargetSelectorState



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
    pid_model_state: Optional[PIDModel] = PIDModel()
    mouse_driver_state: Optional[MouseDriverState] = MouseDriverState()
    target_selector_state: Optional[TargetSelectorState] = TargetSelectorState()