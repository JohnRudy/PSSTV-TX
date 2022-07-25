from typing import Tuple
from enum import Enum

class MODE(Enum):
    ROBOT_36='R36'
    WC_SC2_120='WSC2120'

class SSTV:
    def __init__(cls) -> None:
        pass
    
    @classmethod
    def vis_code(cls, vis:int) -> str:
        """
        Binary of given vis decimal as string
        """
        # TODO:
        # These might be 7 bit... 
        return format(vis,'08b')
    
    @classmethod
    def initial(cls) -> Tuple:
        """
        Start of broadcast.
        """
        # TODO: 
        # Check if viscode affects this
        # I know for a fact that there are different headers for different encoders...
        # Or it's just automation...
        return (
            [1900,1200,1900,1200],
            [300,10,300,30]
        )

    @classmethod
    def sync(cls) -> list[int]:
        """
        Sync pulse at the end of lines
        TODO: Change this to be viscode spesific?
        """
        return [1200, 30]
    
    @classmethod
    def parity(cls) -> list[int]:
        """
        The parity bit
        TODO: Change this to be viscode spesific 
        """
        return [1100,30]

    @classmethod
    def to_chrominance(cls, red:float=0.0,green:float=0.0,blue:float=0.0,luminance:float=0.0) -> list[float]:
        """
        Returns chrominance values as a list of floats [R,G,B]
        """
        chrominance:list[float] = [0.0, 0.0, 0.0]
        chrominance[0] = red - luminance
        chrominance[1] = blue - luminance
        chrominance[2] = luminance - 0.51 * (red - luminance) - 0.19 * (blue - luminance)
        return chrominance
    
    @classmethod
    def to_luminance(cls, red:float=0.0,green:float=0.0,blue:float=0.0) -> float:
        """
        Returns the luminance value of given rgb pixel values
        """
        luminance = float((0.3 * red) + (0.59 * green) + (0.11 * blue))
        return luminance

    @classmethod
    def value_to_hertz(cls, value:float):
        """
        Turns given rgb or ycrcb value to hertz
        """
        hertz = (800 * value) + 1500
        return hertz

    @classmethod
    def scanline(cls,line:list[float], timing_for_pixel:float) -> Tuple:
        """
        Turns a row into hertz and ms values.
        """
        list_hertz:list[float] = []
        list_durations:list[float] = []
        for point in line:
            hertz = SSTV.value_to_hertz(point)
            list_hertz.append(hertz)
            list_durations.append(timing_for_pixel)
        return list_hertz, list_durations

    @classmethod
    def vis_to_hertz(cls,vis_code:str) -> Tuple:
        """
        Turns the vis code into a list of hertz and durations
        """
        # TODO:
        # Different headers might have different values for these...
        hertz:list[float] = []
        duration:list[float] = []
        for i in vis_code:
            if i == 0:
                hertz.append(1300)
            if i == 1:
                hertz.append(1100)
            duration.append(30)
        return hertz, duration

if __name__ == '__main__':
    exit()