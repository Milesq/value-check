from abc import ABC, abstractmethod


class Checkable(ABC):
    @abstractmethod
    def check(self, value) -> bool:
        pass
