from data_center.index import get_data_center
from data_center.models.mouse_driver_model.state import MouseDriverState
from data_center.models.mouse_driver_model.subjects.config import send_config_subject
from data_center.models.mouse_driver_model.subjects.send_vector import send_vector_subject


class MouseDriverSubject:

    @staticmethod
    def send_config(config: MouseDriverState):
        send_config_subject(config)

    @staticmethod
    def send_vector(vector: tuple[float, float]):
        send_vector_subject(vector)

    @staticmethod
    def get_state():
        return get_data_center().get_state().mouse_driver_state