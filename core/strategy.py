from abc import ABC, abstractmethod

class Signal:
    pass


class Strategy(ABC):
    @abstractmethod
    def on_data(self, value) -> Signal:
        pass
