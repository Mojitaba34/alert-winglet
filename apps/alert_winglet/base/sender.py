from abc import ABC, abstractmethod


class BaseSender(ABC):
    @abstractmethod
    def send(self):
        raise NotImplementedError
