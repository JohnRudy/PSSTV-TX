from typing import Tuple

class SSTV:
    def __init__(cls) -> None:
        pass

    """
    Headers and leading tones
    """
    @classmethod
    def vis_code(cls, vis:int) -> str:
        """
        Binary of given vis decimal as string
        """
        # TODO:
        # These might be 7 bit... 
        return format(vis,'07b')
    
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

    """
    Color values
    """
    @classmethod
    def to_luminance(cls, rgb:list[float]) -> float:
        """
        Black and white
        Returns the luminance value of given rgb pixel values.
        """
        luminance = float((0.3 * rgb[0]) + (0.59 * rgb[1]) + (0.11 * rgb[2]))
        return luminance

    @classmethod
    def to_YCrCb(cls, rgb:list[float],luminance:float=0.0) -> list[float]:
        """
        Returns YCrCb values as a list of floats [R,G,B]
        """
        YCrCb:list[float] = [0.0, 0.0, 0.0]
        YCrCb[0] = rgb[0] - luminance
        YCrCb[1] = luminance - 0.51 * (rgb[0] - luminance) - 0.19 * (rgb[2] - luminance)
        YCrCb[2] = rgb[2] - luminance
        return YCrCb
    
    @classmethod
    def to_YRyBy(cls, rgb:list[float]) -> list[float]:
        """
        Takes rgb values band coverts it to a YRyBy format.
        """
        Y = 16.0 + (.003906 * ((65.738 * rgb[0]) + (129.057 * rgb[1]) + (25.064 * rgb[2])))
        RY = 128.0 + (.003906 * ((112.439 * rgb[0]) + (-94.154 * rgb[1]) + (-18.285 * rgb[2])))
        BY = 128.0 + (.003906 * ((-37.945 * rgb[0]) + (-74.494 * rgb[1]) + (112.439 * rgb[2])))
        YRyBy:list[float] = [Y, RY, BY]
        return YRyBy


    """
    Helper methods
    """
    @classmethod
    def float_to_hertz(cls, value:float) -> float:
        """
        Turns given float between 0-1 to hertz value in range of 1500-2300
        """
        hertz = (800 * value/255) + 1500
        return hertz

    @classmethod
    def scanline(cls,line:list[float], timing_for_pixel:float) -> Tuple:
        """
        Turns a row into hertz and ms values.
        """
        list_hertz:list[float] = []
        list_durations:list[float] = []
        for point in line:
            hertz = cls.float_to_hertz(point)
            list_hertz.append(hertz)
            list_durations.append(timing_for_pixel)
        return list_hertz, list_durations

    @classmethod
    def vis_to_hertz(cls,vis_code:str) -> Tuple:
        """
        Turns the vis code into a list of hertz and durations
        """
        # TODO:
        # Different encoders might have different values for these...
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