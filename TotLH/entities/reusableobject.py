from abc import ABC, abstractmethod

class ReusableObject(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def init(self):
        pass