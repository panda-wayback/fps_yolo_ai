
from typing_extensions import Optional
from pydantic import BaseModel
from data_center.models.base_state import BaseState

from data_center.models.screenshot.state import ScreenshotState
from data_center.models.pid_model.state_model import PIDModelState
from data_center.models.yolo_model.state_model import YoloModelState
from data_center.models.mouse_driver_model.state import MouseDriverState
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
    yolo_model_state: Optional[YoloModelState] = YoloModelState()
    screenshot_state: Optional[ScreenshotState] = ScreenshotState()
    pid_model_state: Optional[PIDModelState] = PIDModelState()
    mouse_driver_state: Optional[MouseDriverState] = MouseDriverState()
    target_selector_state: Optional[TargetSelectorState] = TargetSelectorState()