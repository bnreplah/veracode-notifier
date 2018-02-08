from abc import ABC
from abc import abstractmethod


class Action(ABC):
    actions = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.actions.append(cls())

    @abstractmethod
    def pre_action(self, api, s3client, s3bucket):
        pass

    @abstractmethod
    def action(self, api, s3client, s3bucket):
        pass

    @abstractmethod
    def post_action(self, api, s3client, s3bucket):
        pass
