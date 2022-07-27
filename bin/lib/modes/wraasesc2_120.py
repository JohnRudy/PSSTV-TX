from typing import Tuple, List
from bin.lib.modes import MODE
from bin.lib.sstv import SSTV
from numpy import array, ndarray
from tqdm import tqdm, trange
from bin.settings import get_settings
from bin.lib.sstv.encoder_base import BaseEncoder

settings = get_settings(MODE.WC_SC2_120)

class WraaseSC2_120(BaseEncoder):
    def __init__(self, image: ndarray) -> None:
        super().__init__(image)

    # TODO:
    # The audio length is wrong currenyly. Should be over 120 seconds. 1:59 currently.
    def encode(self) -> Tuple:
        """
        Encoding to WraaseSC2-120 standard.
        Returns a tuple (hertz, ms)
        """
        print("----- Beginning turning image to audio data -----")
        self.hertz, self.duration = SSTV.initial()
        vis_code = SSTV.vis_code(settings.VISCode)
        v_hertz, v_dur = SSTV.vis_to_hertz(vis_code)
        self.hertz.extend(v_hertz)
        self.duration.extend(v_dur)
        self.hertz.append(1100)
        self.duration.append(30)
        self.hertz.append(1200)
        self.duration.append(30)


        self.hertz.append(settings.sync_hz['sync pulse'])
        self.duration.append(settings.sync_ms['sync pulse'])
        
        for row in trange(settings.image_size[1]):
            r:list[float] = []
            g:list[float] = []
            b:list[float] = []

            for column in range(settings.image_size[0]):
                r.append(self.image[row,column][0])
                g.append(self.image[row,column][1])
                b.append(self.image[row,column][2])

            # porch
            self.hertz.append(1500)
            self.duration.append(0.5)

            for value in r:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.redblue_pixel_ms)

            for value in g:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.green_pixel_ms)

            for value in b:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.redblue_pixel_ms)

            self.hertz.append(settings.sync_hz['sync pulse'])
            self.duration.append(settings.sync_ms['sync pulse'])

        return self.hertz, self.duration

if __name__ == '__main__':
    exit()
