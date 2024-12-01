from abc import ABC, abstractmethod
from typing import Any


class BaseResource(ABC):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_by_key(self, key: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def get_by_custom_key(self, custom_key: str, value: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def insert_data(self, data_model: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def modify_data(self, data_model: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def delete_data_by_key(self, key: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def delete_data_by_custom_key(self, custom_key: str, value: Any) -> Any:
        raise NotImplementedError()