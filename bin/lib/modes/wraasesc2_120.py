from typing import Tuple, List
from bin.lib.sstv import SSTV, MODE
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
        p_hd = SSTV.parity()
        self.hertz.append(p_hd[0])
        self.duration.append(p_hd[1])
        self.hertz.append(settings.sync_hz['sync pulse'])
        self.duration.append(settings.sync_ms['sync pulse'])
        for row in trange(settings.image_size[1]):
            red:list[float] = []
            green:list[float] = []
            blue:list[float] = []
            for column in range(settings.image_size[0]):
                r = float(self.image[row,column][0])
                g = float(self.image[row,column][1])
                b = float(self.image[row,column][2])
                l = SSTV.to_luminance(r, g, b)
                c = SSTV.to_chrominance(r, g, b, l)
                # These might be wrong, use the rgb values instead? 
                red.append(c[0])
                green.append(c[1])
                blue.append(c[2])
            r_h, r_d = SSTV.scanline(red, settings.redblue_pixel_ms)
            g_h, g_d = SSTV.scanline(green,settings.green_pixel_ms)
            b_h, b_d = SSTV.scanline(blue, settings.redblue_pixel_ms)
            self.hertz.extend(r_h)
            self.hertz.extend(g_h)
            self.hertz.extend(b_h)
            self.duration.extend(r_d)
            self.duration.extend(g_d)
            self.duration.extend(b_d)
            self.hertz.append(settings.sync_hz['sync pulse'])
            self.duration.append(settings.sync_ms['sync pulse'])
        return self.hertz, self.duration

if __name__ == '__main__':
    exit()
