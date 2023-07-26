from abc import ABC, abstractmethod
from typing import Optional


class BaseManager(ABC):
    @abstractmethod
    def format_exception(self) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    def prepare_embed_data(self, formatted_exception: str, extra_detail: Optional[str]):
        ...
