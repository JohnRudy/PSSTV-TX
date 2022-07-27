from PIL import Image
import numpy as np
from numpy import ndarray
from bin.lib.modes import MODE
from bin.settings import get_settings

class ImageAsArray:
    def to_array(path:str, mode:MODE) -> ndarray:
        """
        Returns an np.array of floats of given image path between 0 and 1
        """
        size = get_settings(mode).image_size
        img = Image.open(path)

        if img.size != size:
            img = img.resize(size,resample=0,box=None)
        
        img = img.convert('RGB')
        img = np.asarray(img,dtype=np.int32)
        return img

if __name__ == '__main__':
    exit()