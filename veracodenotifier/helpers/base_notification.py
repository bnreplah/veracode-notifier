from abc import ABC
from abc import abstractmethod


class Notification(ABC):
    notifications = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.notifications.append(cls())

    @abstractmethod
    def send_notification(self):
        pass
