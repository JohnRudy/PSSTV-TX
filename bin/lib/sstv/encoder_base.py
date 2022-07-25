from typing import Protocol, Tuple
from numpy import ndarray

class Encoder(Protocol):
    def encode() -> Tuple:
        """
        Preparing for future.
        All encoders need to have this method. 
        """
        ...

class BaseEncoder:
    def __init__(self, image:ndarray) -> None:
        """
        Base class for all encoders
        """
        self.image:ndarray = image
        self.hertz:list[float] = []
        self.duration:list[float] = []
    
    def encode(self) -> Tuple:
        ...