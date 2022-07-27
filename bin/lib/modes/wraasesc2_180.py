from typing import Tuple, List
from bin.lib.sstv import SSTV, MODE
from numpy import array, ndarray
from tqdm import tqdm, trange
from bin.settings import get_settings
from bin.lib.sstv.encoder_base import BaseEncoder

settings = get_settings(MODE.WC_SC2_180)

class WraaseSC2_180(BaseEncoder):
    def __init__(self, image: ndarray) -> None:
        super().__init__(image)

    def encode(self) -> Tuple:
        """
        Encoding to WraaseSC2-180 standard.
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

        for row in trange(settings.image_size[1]):
            y:list[float] = []
            ry:list[float] = []
            by:list[float] = []

            for column in range(settings.image_size[0]):
                YRyBy = SSTV.to_YRyBy(self.image[row,column])
                y.append(YRyBy[0])
                ry.append(YRyBy[1])
                by.append(YRyBy[2])

            self.hertz.append(settings.sync_hz['sync pulse'])
            self.duration.append(settings.sync_ms['sync pulse'])

            self.hertz.append(settings.sync_hz['sync porch'])
            self.duration.append(settings.sync_ms['sync porch'])

            for value in y:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.pixle_time)

            for value in ry:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.pixle_time)

            for value in by:
                self.hertz.append(SSTV.float_to_hertz(value))
                self.duration.append(settings.pixle_time)

        return self.hertz, self.duration

if __name__ == '__main__':
    exit()
